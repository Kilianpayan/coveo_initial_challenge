package codes.blitz.challenge.bot;

import codes.blitz.challenge.generated.Action;
import codes.blitz.challenge.generated.AddBiomassAction;
import codes.blitz.challenge.generated.Position;
import codes.blitz.challenge.generated.RemoveBiomassAction;
import codes.blitz.challenge.generated.TeamGameState;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Bot {
  Random random = new Random();

  public Bot() {
    System.out.println("Initializing your super duper mega bot");
  }

  /*
   * Here is where the magic happens, for now the moves are random. I bet you can do better ;)
   */
  public List<Action> getActions(TeamGameState gameMessage) {
    List<Action> actions = new ArrayList<>();

    // Pick a number of biomass to move this turn.
    int remainingBiomassToMoveThisTurn = randomInt(1, gameMessage.maximumNumberOfBiomassPerTurn());

    while (remainingBiomassToMoveThisTurn > 0) {
      Position randomPosition =
          new Position(
              randomInt(0, gameMessage.map().width() - 1),
              randomInt(0, gameMessage.map().height() - 1));

      // Randomly decide whether to add or remove biomass
      boolean shouldAddBiomass = randomInt(0, 1) == 1;

      if (shouldAddBiomass) {
        int biomassToMoveInThisAction = randomInt(1, remainingBiomassToMoveThisTurn);
        remainingBiomassToMoveThisTurn -= biomassToMoveInThisAction;

        actions.add(new AddBiomassAction(biomassToMoveInThisAction, randomPosition));
      } else {
        int biomassToMoveInThisAction =
            Math.min(
                remainingBiomassToMoveThisTurn,
                gameMessage.map().biomass()[randomPosition.x()][randomPosition.y()]);
        remainingBiomassToMoveThisTurn -= biomassToMoveInThisAction;

        actions.add(new RemoveBiomassAction(biomassToMoveInThisAction, randomPosition));
      }
    }

    // You can clearly do better than the random actions above. Have fun!!
    return actions;
  }

  private int randomInt(int min, int max) {
    return random.nextInt(max - min + 1) + min;
  }
}
