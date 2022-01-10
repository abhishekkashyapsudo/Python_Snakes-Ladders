config.json will contain all the configurations required for the game.

    => board: will contain the side length for the board

    => snakes: it will contain an array specifying the start and end for the snakes
    => ladders: it will contain an array specifying the start and end for the ladders

    => dice: it will contain an array specifying the numbers that can be rolled.

Validations:
    board:
        => side of a board can not be less than 5, and it can't be greater than 15. 
        => The game will be terminated after printing an error message if such condition is encountered.

    snakes:
        => Start for a snake cannot be less than the end. 
        => Start or end must be valid. (greater than/equal to 0 and less than the target).
        => Any snake with such config will be skipped.

    ladders:
        => Start for a ladder cannot be greater than the end. 
        => Start or end must be valid. (greater than/equal to 0 and less than the target).
        => Any ladder with such config will be skipped.

    dice:
        => A dice must have minimum 4 values.
        => A dice can't have a negative value, zero or a value greater than 8.
        => Two sides of the dice can't be same.
        => An extra turn will ge given on getting a 6.
        => The game will be terminated after printing an error message if such condition is encountered.
        

    