namespace Application;

public class Bot
{
    public const string NAME = "My cool C# bot";

    /// <summary>
    /// This method should be used to initialize some variables you will need throughout the game.
    /// </summary>
    public Bot()
    {
        Console.WriteLine("Initializing your super duper mega bot");
    }

    /// <summary>
    /// Here is where the magic happens, for now the moves are random. I bet you can do better ;)
    /// </summary>
    public IEnumerable<Action> GetNextMoves(TeamGameState gameMessage)
    {
        var actions = new List<Action>();

        // Pick a number of biomass to move this turn.
        var remainingBiomassToMoveThisTurn = RandomInt(
            1,
            gameMessage.MaximumNumberOfBiomassPerTurn
        );

        while (remainingBiomassToMoveThisTurn > 0)
        {
            var randomPosition = new Position(
                RandomInt(0, gameMessage.Map.Width - 1),
                RandomInt(0, gameMessage.Map.Height - 1)
            );

            // Randomly decide whether to add or remove biomass
            var shouldAddBiomass = RandomInt(0, 1) == 1;

            if (shouldAddBiomass)
            {
                var biomassToMoveInThisAction = RandomInt(1, remainingBiomassToMoveThisTurn);
                remainingBiomassToMoveThisTurn -= biomassToMoveInThisAction;

                actions.Add(new AddBiomassAction(biomassToMoveInThisAction, randomPosition));
            }
            else
            {
                var biomassToMoveInThisAction = Math.Min(
                    remainingBiomassToMoveThisTurn,
                    gameMessage.Map.Biomass[randomPosition.X][randomPosition.Y]
                );
                remainingBiomassToMoveThisTurn -= biomassToMoveInThisAction;

                actions.Add(new RemoveBiomassAction(biomassToMoveInThisAction, randomPosition));
            }
        }

        // You can clearly do better than the random actions above. Have fun!!
        return actions;
    }

    private static int RandomInt(int min, int max)
    {
        return Random.Shared.Next(min, max + 1);
    }
}
