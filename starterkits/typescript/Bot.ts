import { Action, ActionType, TeamGameState, ActionAddBiomass, ActionRemoveBiomass } from './GameInterface';

export class Bot {
    constructor() {
        console.log('Initializing your super duper mega bot');
    }

    getNextMoves(gameMessage: TeamGameState): Action[] {
        const actions: Action[] = [];

        // Pick a number of biomass to move this turn.
        let remainingBiomassToMoveThisTurn = randomInt(1, gameMessage.maximumNumberOfBiomassPerTurn);

        while (remainingBiomassToMoveThisTurn > 0) {
            const randomPosition = {
                x: randomInt(0, gameMessage.map.width - 1),
                y: randomInt(0, gameMessage.map.height - 1)
            };

            // Randomly decide whether to add or remove biomass
            const shouldAddBiomass = randomInt(0, 1) === 1;

            if (shouldAddBiomass) {
                const biomassToMoveInThisAction = randomInt(1, remainingBiomassToMoveThisTurn);
                remainingBiomassToMoveThisTurn -= biomassToMoveInThisAction;

                actions.push({
                    type: ActionType.ADD_BIOMASS,
                    position: randomPosition,
                    amount: biomassToMoveInThisAction
                } as ActionAddBiomass);
            } else {
                const biomassToMoveInThisAction = Math.min(
                    remainingBiomassToMoveThisTurn,
                    gameMessage.map.biomass[randomPosition.x][randomPosition.y]
                );
                remainingBiomassToMoveThisTurn -= biomassToMoveInThisAction;

                actions.push({
                    type: ActionType.REMOVE_BIOMASS,
                    position: randomPosition,
                    amount: biomassToMoveInThisAction
                } as ActionRemoveBiomass);
            }
        }

        // You can clearly do better than the random actions above. Have fun!!
        return actions;
    }
}

function randomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
