'''
TTP Evaluation on ImageNet validation.
For each target, we have 49950 samples of the other classes.
'''

import argparse
import os

import torchvision
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transforms

import torchvision.models as models
from generators import GeneratorResnet
from gaussian_smoothing import *

# Purifier
from NRP import *

import logging
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Targeted Transferable Perturbations')
parser.add_argument('--test_dir', default='../../../data/IN/val')
parser.add_argument('--batch_size', type=int, default=20, help='Batch size for evaluation')
parser.add_argument('--eps', type=int, default=16, help='Perturbation Budget')
parser.add_argument('--target_model', type=str, default='vgg19_bn', help='Black-Box(unknown) model: SIN, Augmix')
parser.add_argument('--target', type=int, default=99, help='Target label to transfer')
parser.add_argument('--source_model', type=str, default='res50', help='TTP Discriminator: \
{res18, res50, res101, res152, dense121, dense161, dense169, dense201,\
 vgg11, vgg11_bn, vgg13, vgg13_bn, vgg16, vgg16_bn, vgg19, vgg19_bn,\
 ens_vgg16_vgg19_vgg11_vgg13_all_bn,\
 ens_res18_res50_res101_res152\
 ens_dense121_161_169_201}')
parser.add_argument('--source_domain', type=str, default='IN', help='Source Domain (TTP): Natural Images (IN) or painting')


# For purification (https://github.com/Muzammal-Naseer/NRP)
parser.add_argument('--NRP', action='store_true', help='Apply Neural Purification to reduce adversarial effect')
args = parser.parse_args()
print(args)

# GPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Set-up log file
logfile = '10T_subsrc/TTP_10_target_eval_eps_{}_{}_to_{}_NRP_{}.log'.format(args.eps, args.source_model, args.target_model, args.NRP)
logging.basicConfig(
    format='[%(asctime)s] - %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO,
    filename=logfile)

eps = args.eps/255.0

# Set-up Kernel
kernel_size = 3
pad = 2
sigma = 1
kernel = get_gaussian_kernel(kernel_size=kernel_size, pad=pad, sigma=sigma).cuda()


# Load pretrained Generator
netG = GeneratorResnet()
netG.load_state_dict(torch.load('pretrained_generators/netG_{}_{}_19_{}.pth'.format(args.source_model,args.source_domain, args.target)))
netG = netG.to(device)
netG.eval()

# Load Targeted Model
model_names = sorted(name for name in models.__dict__
    if name.islower() and not name.startswith("__")
    and callable(models.__dict__[name]))

if args.target_model in model_names:
    model = models.__dict__[args.target_model](pretrained=True)
elif args.target_model == 'SIN':
    model = torchvision.models.resnet50(pretrained=False)
    model = torch.nn.DataParallel(model)
    checkpoint = torch.load('pretrained_models/resnet50_train_60_epochs-c8e5653e.pth.tar')
    model.load_state_dict(checkpoint["state_dict"])
elif args.target_model == 'Augmix':
    model = torchvision.models.resnet50(pretrained=False)
    model = torch.nn.DataParallel(model)
    checkpoint = torch.load('pretrained_models/checkpoint.pth.tar')
    model.load_state_dict(checkpoint["state_dict"])
else:
    assert (args.target_model in model_names), 'Please provide correct target model names: {}'.format(model_names)

model = model.to(device)
model.eval()


if args.NRP:
    purifier = NRP(3, 3, 64, 23)
    purifier.load_state_dict(torch.load('pretrained_purifiers/NRP.pth'))
    purifier = purifier.to(device)

####################
# Data
####################
# Input dimensions
scale_size = 256
img_size = 224
data_transform = transforms.Compose([
    transforms.Resize(scale_size),
    transforms.CenterCrop(img_size),
    transforms.ToTensor(),
])

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
def normalize(t):
    t[:, 0, :, :] = (t[:, 0, :, :] - mean[0])/std[0]
    t[:, 1, :, :] = (t[:, 1, :, :] - mean[1])/std[1]
    t[:, 2, :, :] = (t[:, 2, :, :] - mean[2])/std[2]

    return t

test_dir = args.test_dir
test_set = datasets.ImageFolder(test_dir, data_transform)

# Remove samples that belong to the target attack label.
source_samples = []
for img_name, label in test_set.samples:
    if label != args.target:
        source_samples.append((img_name, label))
test_set.samples = source_samples
test_loader = torch.utils.data.DataLoader(test_set, batch_size=args.batch_size, shuffle=False, num_workers=4,
                                              pin_memory=True)

test_size = len(test_set)
print('Test data size:', test_size)

acc = 0
distance = 0

logger.info('Epsilon \t Target \t Acc. \t Distance')
for i, (img, label) in enumerate(test_loader):
    print('At Batch:', i)
    img, label = img.to(device), label.to(device)

    target_label = torch.LongTensor(img.size(0))
    target_label.fill_(args.target)
    target_label = target_label.to(device)

    adv = kernel(netG(img)).detach()
    adv = torch.min(torch.max(adv, img - eps), img + eps)
    adv = torch.clamp(adv, 0.0, 1.0)

    if args.NRP:
        # Purify Adversary
        adv = purifier(adv).detach()

    out = model(normalize(adv.clone().detach()))
    acc += torch.sum(out.argmax(dim=-1) == target_label).item()

    distance +=(img - adv).max() *255


logger.info(' %d             %d\t  %.4f\t \t %.4f',
            int(eps * 255), args.target, acc / test_size, distance / (i + 1))
