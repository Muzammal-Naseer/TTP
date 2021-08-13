import argparse
import os
import numpy as np

import torchvision
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import torchvision.models as models

from generators import *
from gaussian_smoothing import *

from utils import TwoCropTransform, rotation


parser = argparse.ArgumentParser(description='Transferable Targeted Perturbations')
parser.add_argument('--src', default='paintings', help='Source Domain: natural images, paintings, medical scans, etc')
parser.add_argument('--match_target', type=int, default=3, help='Target Domain samples')
parser.add_argument('--match_dir', default= '../../data/IN_per_class/', help='Path to data folder with target domain samples')
parser.add_argument('--batch_size', type=int, default=20, help='Number of trainig samples/batch')
parser.add_argument('--epochs', type=int, default=20, help='Number of training epochs')
parser.add_argument('--lr', type=float, default=0.0002, help='Initial learning rate for adam')
parser.add_argument('--eps', type=int, default=10, help='Perturbation Budget during training, eps')
parser.add_argument('--model_type', type=str, default='resnet50',
                    help='Model under attack (discrimnator)')
parser.add_argument('--gs', action='store_true', help='Apply gaussian smoothing')
parser.add_argument('--save_dir', type=str, default='pretrained_generators_retrain', help='Directory to save generators')
args = parser.parse_args()
print(args)


if not os.path.isdir(args.save_dir):
    os.mkdir(args.save_dir)


eps = args.eps / 255

# GPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


# Discriminator
model_names = sorted(name for name in models.__dict__
    if name.islower() and not name.startswith("__")
    and callable(models.__dict__[name]))

if args.model_type in model_names:
    model = models.__dict__[args.model_type](pretrained=True)
else:
    assert (args.model_type in model_names), 'Please provide correct target model names: {}'.format(model_names)


model = model.to(device)
model.eval()


# Input dimensions
if args.model_type == 'inception_v3':
    scale_size = 300
    img_size = 299
else:
    scale_size = 256
    img_size = 224


# Generator
if args.model_type == 'inception_v3':
    netG = GeneratorResnet(inception=True)
else:
    netG = GeneratorResnet()
netG.to(device)

# Optimizer
optimG = optim.Adam(netG.parameters(), lr=args.lr, betas=(0.5, 0.999))
torchvision.transforms.PILToTensor()
# Data
train_transform = transforms.Compose([
    transforms.Resize(scale_size),
    transforms.CenterCrop(img_size),
    transforms.ToTensor()])

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

def normalize(t):
    t[:, 0, :, :] = (t[:, 0, :, :] - mean[0]) / std[0]
    t[:, 1, :, :] = (t[:, 1, :, :] - mean[1]) / std[1]
    t[:, 2, :, :] = (t[:, 2, :, :] - mean[2]) / std[2]
    return t


train_set = torchvision.datasets.ImageFolder(args.src, TwoCropTransform(train_transform, img_size))
train_loader = torch.utils.data.DataLoader(train_set, batch_size=args.batch_size, shuffle=True, num_workers=4,
                                           pin_memory=True)
train_size = len(train_set)
print('Training data size:', train_size)

# Imagenet folder to label mapping
target_dict = { 3 : 'n01491361',
               16 : 'n01560419',
               24 : 'n01622779',
               36 : 'n01667778',
               48 : 'n01695060',
               52 : 'n01728572',
               69 : 'n01768244',
               71 : 'n01770393',
               85 : 'n01806567',
               99 : 'n01855672',
               107 : 'n01910747',
               114 : 'n01945685',
               130 : 'n02007558',
               138 : 'n02018795',
               142 : 'n02033041',
               151 : 'n02085620',
               162 : 'n02088364',
               178 : 'n02092339',
               189 : 'n02095570',
               193 : 'n02096294',
               207 : 'n02099601',
               212 : 'n02100735',
               228 : 'n02105505',
               240 : 'n02107908',
               245 : 'n02108915',
               260 : 'n02112137',
               261 : 'n02112350',
               276 : 'n02117135',
               285 : 'n02124075',
               291 : 'n02129165',
               309 : 'n02206856',
               317 : 'n02259212',
               328 : 'n02319095',
               340 : 'n02391049',
               344 : 'n02398521',
               358 : 'n02443114',
               366 : 'n02480855',
               374 : 'n02488291',
               390 : 'n02526121',
               393 : 'n02607072',
               404 : 'n02690373',
               420 : 'n02787622',
               430 : 'n02802426',
               438 : 'n02815834',
               442 : 'n02825657',
               453 : 'n02870880',
               464 : 'n02910353',
               471 : 'n02950826',
               485 : 'n02988304',
               491 : 'n03000684',
               506 : 'n03065424',
               513 : 'n03110669',
               523 : 'n03141823',
               538 : 'n03220513',
               546 : 'n03272010',
               555 : 'n03345487',
               569 : 'n03417042',
               580 : 'n03457902',
               582 : 'n03461385',
               599 : 'n03530642',
               605 : 'n03584254',
               611 : 'n03598930',
               629 : 'n03676483',
               638 : 'n03710637',
               646 : 'n03733281',
               652 : 'n03763968',
               661 : 'n03777568',
               678 : 'n03814639',
               689 : 'n03866082',
               701 : 'n03888257',
               707 : 'n03902125',
               717 : 'n03930630',
               724 : 'n03947888',
               735 : 'n03980874',
               748 : 'n04026417',
               756 : 'n04049303',
               766 : 'n04111531',
               779 : 'n04146614',
               786 : 'n04179913',
               791 : 'n04204347',
               802 : 'n04252077',
               813 : 'n04270147',
               827 : 'n04330267',
               836 : 'n04355933',
               849 : 'n04398044',
               859 : 'n04442312',
               866 : 'n04465501',
               879 : 'n04507155',
               885 : 'n04525038',
               893 : 'n04548362',
               901 : 'n04579145',
               919 : 'n06794110',
               929 : 'n07615774',
               932 : 'n07695742',
               946 : 'n07730033',
               958 : 'n07802026',
               963 : 'n07873807',
               980 : 'n09472597',
               984 : 'n11879895',
               992 : 'n12998815'
}

args.match_dir = os.path.join(args.match_dir, target_dict[args.match_target])

train_set_match = torchvision.datasets.ImageFolder(args.match_dir, train_transform)
if len(train_set_match) < 1300:
    train_set_match.samples = train_set_match.samples[0:1000]
train_loader_match = torch.utils.data.DataLoader(train_set_match, batch_size=args.batch_size, shuffle=True, num_workers=2,
                                           pin_memory=True)
train_size_match = len(train_set_match)
print('Training (Match) data size:', train_size_match)
# Iterator
dataiter = iter(train_loader_match)


if args.gs:
    kernel_size = 3
    pad = 2
    sigma = 1
    kernel = get_gaussian_kernel(kernel_size=kernel_size, pad=pad, sigma=sigma).cuda()


criterion_kl = nn.KLDivLoss(size_average=False)
cosine = torch.nn.CosineSimilarity(dim=1, eps=1e-08)
for epoch in range(args.epochs):
    running_loss = 0
    for i, (imgs, _) in enumerate(train_loader):
        img = imgs[0].to(device)
        img_rot = rotation(img)[0]
        img_aug = imgs[1].to(device)

        try:
            img_match = next(dataiter)[0]
        except StopIteration:
            dataiter = iter(train_loader_match)
            img_match = next(dataiter)[0]
        img_match = img_match.to(device)

        netG.train()
        optimG.zero_grad()

        # Unconstrained Adversaries
        adv = netG(img)
        adv_rot = netG(img_rot)
        adv_aug = netG(img_aug)

        # Smoothing
        if args.gs:
            adv = kernel(adv)
            adv_rot = kernel(adv_rot)
            adv_aug = kernel(adv_aug)


        # Projection
        adv = torch.min(torch.max(adv, img - eps), img + eps)
        adv = torch.clamp(adv, 0.0, 1.0)
        adv_rot = torch.min(torch.max(adv_rot, img_rot - eps), img_rot + eps)
        adv_rot = torch.clamp(adv_rot, 0.0, 1.0)
        adv_aug = torch.min(torch.max(adv_aug, img_aug - eps), img_aug + eps)
        adv_aug = torch.clamp(adv_aug, 0.0, 1.0)

        adv_out = model(normalize(adv))
        adv_rot_out = model(normalize(adv_rot))
        adv_aug_out = model(normalize(adv_aug))
        img_match_out = model(normalize(img_match))


        # Loss
        loss_kl = 0.0
        loss_sim  = 0.0
        for out in [adv_out, adv_rot_out, adv_aug_out]:

            loss_kl += (1.0 / args.batch_size) * criterion_kl(F.log_softmax(out, dim=1),
                                                             F.softmax(img_match_out, dim=1))
            loss_kl += (1.0 / args.batch_size) * criterion_kl(F.log_softmax(img_match_out, dim=1),
                                                               F.softmax(out, dim=1))

        # Neighbourhood similarity
        St = torch.matmul(img_match_out,  img_match_out.t())
        norm = torch.matmul(torch.linalg.norm(img_match_out, dim=1, ord=2), torch.linalg.norm(img_match_out, dim=1, ord=2).t())
        St = St/norm
        for out in [adv_rot_out, adv_aug_out]:
            Ss = torch.matmul(adv_out,  out.t())
            norm = torch.matmul(torch.linalg.norm(adv_out, dim=1, ord=2), torch.linalg.norm(out, dim=1, ord=2).t())
            Ss = Ss/norm
            loss_sim += (1.0 / args.batch_size) * criterion_kl(F.log_softmax(Ss, dim=1),
                                                             F.softmax(St, dim=1))
            loss_sim += (1.0 / args.batch_size) * criterion_kl(F.log_softmax(St, dim=1),
                                                               F.softmax(Ss, dim=1))

        loss = loss_kl + loss_sim
        loss.backward()
        optimG.step()
        running_loss += loss.item()

        if i % 10 == 9:
            print('Epoch: {0} \t Batch: {1} \t loss: {2:.5f}'.format(epoch, i, running_loss / 10))
            running_loss = 0

    torch.save(netG.state_dict(),args.save_dir + '/netG_{}_{}_{}.pth'.format(args.model_type, epoch, args.match_target))
