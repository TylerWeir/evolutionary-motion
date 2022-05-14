# Evolutionary Mace Balancing
Train AI agents to perform mace balancing using an evolutionary neural network.

## Background

"Mace balancing" involves applying some (limited) force to a base that is supporting a pole, such that the pole does not fall over, with the added challenge of a heavy chain hanging off the end of the pole. This chain massively increases the chaos of the system and makes the balancing act a much harder problem than simple pole balancing.

We employ a mutation-and-selection evolutionary algorithm to create highly capable mace balancing agents.

The agents make decisions frame-by-frame about how much "effort" to apply to move their base and in what direction. This "effort" value is unbounded, but is passed through a tanh function and scaled according to their "strength" property, to mimic the way that a living being applies force in the real world.

The decision process is executed with a custom coded neural network.

Each generation, gaussian noise with a certain standard deviation is applied to all the weights in the top networks. The number of networks chosen for reproduction is specified with the -r command line argument. In our experimentation, roughly 10-20% of the total number of agents seems to work best.

## Example Results

The following shows training for 200 epochs with 200 agents, 10% random mixins, and 10 agents selected for reproduction each epoch.

As you can see, by epoch 200 (but not earlier!) all 180 agents that are not random mixins reach 5000 score, indicating success.

![out2](https://user-images.githubusercontent.com/56745633/168406539-62ffaa14-67ea-422e-9ac7-3e2afe6ee830.gif)


Here's how the best network from the above training session performs:
![reallygoodnet](https://user-images.githubusercontent.com/56745633/168406853-8b0fc98e-ba83-428a-aea4-0ffcff70942e.gif)

## Usage
| Argument     | Type  |Description |
|--------------|-------|------------|
|-h, --help    |  n/a  |  Shows the help message |
|-a, -agents    |  integer | The number of agents to simulate |
|-r, --reproducers | integer | The number of agents that reproduce after each round|
|-e, --epochs| integer | The number of epochs to train the agents for |
|-c, --chainlength | integer | The number of additional segments to add onto the ends of the rods |
|-n, --nographics | n/a | Disable graphics which allows for much faster training |
|-l, --loadname | String | Filepath to a network file to load. Will not train the loaded network |
|-s, --savename | String | Filepath to the file the best network will be saved in |
