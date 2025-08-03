# Tetris Game Machine Learning

A classic Tetris implementation built using Claude Code with as little prompting details as possible using Python and Pygame, featuring all standard gameplay mechanics. Machine learning is used to let AI play the game. The code was written using two very minimal prompts lacking detailed info (purposely so)

**prompt 1**) Build a game of tetris in python with pygame. Ensure that the controls are in a seperate file, so that has actions like left, right, down, etc. Just like tetris, with 7 tetrimino types

**prompt 2**) I want AI to play Tetris now. Use the existing code, but change the controls to AI. It needs to learn to play tetris and the attached images describe the two features to use. I want the user to be able to tweak the values from -10 to 10 to find the optimal penalty/reward values

![hole.png](images/holes.png)

![landing height.png](images/landingheight.png)

-----
Notice I did not specify any details about what kind of machine learning to use. I did this on purpose. I want to learn and I think most of this is well known. Later on I'll figure out what it did so I can learn what choices it made.

## Results

![recording.gif](images/recording.gif)


Interstingly enough it added two feature that I did not specify at all: "Lines Cleared" and "Bumpiness". I tweaked the values in the recording shown above to do well enough. I'm not interested in perfection for this project.

So now, let's as Claude to explain the machine learning part of the code by feeding it to claude.ai with this prompt:

**prompt**) You wrote this code. Explain to me the choices that you've made on the machine learning side. Please keep it concise

Result:

Looking at this Tetris AI code, here are the key ML design choices I made:

## Architecture & Algorithm
- **Deep Q-Network (DQN)** with target network for stable learning
- **3-layer fully connected network** (512→512→256→actions) with ReLU activations and dropout
- **Experience replay buffer** (50k capacity) to break temporal correlations

## State Representation
**Engineered features** rather than raw pixels:
- Height profile of each column (10 values)
- Aggregate metrics: total height, holes, bumpiness, complete lines
- Current/next piece encoding
- Game progress indicators
- **Total: ~20 features** - compact but informative

## Reward Design
**Shaped rewards** for faster learning:
- Large rewards for line clears (10-100 points, exponential for multiple lines)
- Penalties for holes (-2 per hole) and height increases (-0.5 per unit)
- **Bumpiness penalty** (tunable) to encourage flat surfaces
- Small survival bonus (+0.01) and large game-over penalty (-100)

## Training Optimizations
- **GPU acceleration** with mixed precision training
- **Gradient clipping** (norm=1.0) for stability
- **Learning rate scheduling** (decay every 1000 steps)
- **Larger batch sizes** on GPU (64 vs 32 CPU)
- **Real-time parameter tuning** via sliders

## Key Design Philosophy
Chose **interpretable features over raw pixels** for faster convergence and **heavily shaped rewards** rather than sparse signals. The bumpiness penalty was particularly important - it teaches the AI to create flat surfaces, which is crucial for Tetris success but hard to learn from game score alone.
