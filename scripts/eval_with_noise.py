"""Run ``lerobot-eval`` with Gaussian noise added to every executed action.

This creates a controlled "worse" policy variant for evallog demos: the
policy is unchanged, but each action sent to the simulator gets
N(0, sigma^2) noise on the arm dimensions (the gripper is left alone).

Usage (same arguments as lerobot-eval):
    NOISE_STD=0.1 NOISE_SEED=0 python scripts/eval_with_noise.py \
        --policy.path=lerobot/pi05_libero_finetuned --env.type=libero \
        --env.task=libero_10 --policy.n_action_steps=10 \
        --eval.n_episodes=50 --eval.batch_size=1 --output_dir=outputs/noise_010

NOISE_STD   standard deviation of the noise (LIBERO actions are in [-1, 1]).
NOISE_SEED  base seed; episode k always gets the same noise for a given seed.
NOISE_DIMS  how many leading action dimensions get noise (default 6: the
            arm's position and rotation deltas, not the gripper).
"""

import os

import numpy as np

NOISE_STD = float(os.environ.get("NOISE_STD", "0.1"))
NOISE_SEED = int(os.environ.get("NOISE_SEED", "0"))
NOISE_DIMS = int(os.environ.get("NOISE_DIMS", "6"))


def add_noise(action, rng, std=NOISE_STD, dims=NOISE_DIMS):
    """Return a copy of a (batch, action_dim) action with noise on the first dims."""
    noisy = np.array(action, dtype=np.float64, copy=True)
    noisy[:, :dims] += rng.normal(0.0, std, size=noisy[:, :dims].shape)
    noisy[:, :dims] = np.clip(noisy[:, :dims], -1.0, 1.0)
    return noisy.astype(np.asarray(action).dtype)


def wrap_rollout(original_rollout):
    """Wrap LeRobot's rollout so env.step receives noisy actions."""
    counter = {"episode": 0}

    def noisy_rollout(env, *args, **kwargs):
        rng = np.random.default_rng([NOISE_SEED, counter["episode"]])
        counter["episode"] += 1
        original_step = env.step

        def step(action):
            return original_step(add_noise(action, rng))

        env.step = step
        try:
            return original_rollout(env, *args, **kwargs)
        finally:
            env.step = original_step

    return noisy_rollout


def main():
    from lerobot.scripts import lerobot_eval

    print(f"[eval_with_noise] std={NOISE_STD} seed={NOISE_SEED} dims={NOISE_DIMS}", flush=True)
    lerobot_eval.rollout = wrap_rollout(lerobot_eval.rollout)
    lerobot_eval.main()


if __name__ == "__main__":
    main()
