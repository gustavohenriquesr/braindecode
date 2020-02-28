"""
Trialwise Decoding on BCIC IV 2a Competition Set with skorch and moabb.
=====================================================================
"""

# Authors: Maciej Sliwowski <maciek.sliwowski@gmail.com>
#          Robin Tibor Schirrmeister <robintibor@gmail.com>
#          Lukas Gemein <l.gemein@gmail.com>
#          Hubert Banville <hubert.jbanville@gmail.com>
#
# License: BSD-3
from collections import OrderedDict
from functools import partial

import numpy as np
import torch
import mne
from skorch.callbacks import LRScheduler
from skorch.callbacks.scoring import EpochScoring
mne.set_log_level('ERROR')

from braindecode.datautil.windowers import create_windows_from_events
from braindecode.classifier import EEGClassifier
from braindecode.datasets import MOABBDataset
from braindecode.models.deep4 import Deep4Net
from braindecode.models.shallow_fbcsp import ShallowFBCSPNet
from braindecode.scoring import PostEpochTrainScoring
from braindecode.util import set_random_seeds
from braindecode.datautil.signalproc import exponential_running_standardize
from braindecode.datautil.transforms import transform_concat_ds

subject_id = 3  # 1-9
model_name = "shallow"  # 'shallow' or 'deep'
low_cut_hz = 4.  # 0 or 4
n_epochs = 5
seed = 20200220

high_cut_hz = 38.
trial_start_offset_seconds = -0.5
input_time_length = 1125
batch_size = 64
factor_new = 1e-3
init_block_size = 1000
cuda = torch.cuda.is_available()
device = 'cuda' if cuda else 'cpu'
if cuda:
    torch.backends.cudnn.benchmark = True

n_classes = 4
n_chans = 22

set_random_seeds(seed=seed, cuda=cuda)

if model_name == "shallow":
    model = ShallowFBCSPNet(
        n_chans,
        n_classes,
        input_time_length=input_time_length,
        final_conv_length='auto',
    )
    lr = 0.0625 * 0.01
    weight_decay = 0

elif model_name == "deep":
    model = Deep4Net(
        n_chans,
        n_classes,
        input_time_length=input_time_length,
        final_conv_length='auto',
    )
    lr = 1 * 0.01
    weight_decay = 0.5 * 0.001

if cuda:
    model.cuda()

dataset = MOABBDataset(dataset_name="BNCI2014001", subject_ids=[subject_id])

standardize_func = partial(
    exponential_running_standardize, factor_new=factor_new,
    init_block_size=init_block_size)
raw_transform_dict = OrderedDict([
    ("pick_types", dict(eeg=True, meg=False, stim=False)),
    ('apply_function', dict(fun=lambda x: x * 1e6, channel_wise=False)),
    ('filter', dict(l_freq=low_cut_hz, h_freq=high_cut_hz)),
    ('apply_function', dict(fun=standardize_func, channel_wise=False))
])
transform_concat_ds(dataset, raw_transform_dict)

sfreqs = [ds.raw.info['sfreq'] for ds in dataset.datasets]
assert len(np.unique(sfreqs)) == 1
trial_start_offset_samples = int(trial_start_offset_seconds * sfreqs[0])

windows_dataset = create_windows_from_events(
    dataset,
    trial_start_offset_samples=trial_start_offset_samples,
    trial_stop_offset_samples=0,
    supercrop_size_samples=input_time_length,
    supercrop_stride_samples=input_time_length,
    drop_samples=False,
    preload=True,
)

class TrainTestBCICIV2aSplit(object):
    def __call__(self, dataset, y, **kwargs):
        splitted = dataset.split('session')
        return splitted['session_T'], splitted['session_E']

cb_train_acc = PostEpochTrainScoring(
    "accuracy",
    name="train_trial_accuracy",
    lower_is_better=False,
)
cb_valid_acc = EpochScoring(
    "accuracy",
    name="valid_trial_accuracy",
    lower_is_better=False,
    on_train=False,
)
# MaxNormDefaultConstraint and early stopping should be added to repeat
# previous braindecode

clf = EEGClassifier(
    model,
    criterion=torch.nn.NLLLoss,
    optimizer=torch.optim.AdamW,
    train_split=TrainTestBCICIV2aSplit(),
    optimizer__lr=lr,
    optimizer__weight_decay=weight_decay,
    iterator_train__shuffle=True,
    batch_size=batch_size,
    callbacks=[
        ("train_trial_accuracy", cb_train_acc),
        ("valid_trial_accuracy", cb_valid_acc),
        # seems n_epochs -1 leads to desired behavior of lr=0 after end of training?
        ("lr_scheduler",
         LRScheduler('CosineAnnealingLR', T_max=n_epochs - 1)),
    ],
    device=device,
)

clf.fit(windows_dataset, y=None, epochs=n_epochs)