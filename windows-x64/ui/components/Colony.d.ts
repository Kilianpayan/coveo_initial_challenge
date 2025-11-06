import { FC } from 'react';
import type { Colony } from '../GameInterface';
import type { ViewerGameState } from '../ViewerTypes';
import { Constants } from './PlayZone';
interface ColonySpriteProps {
    colony: Colony;
    constants: Constants;
    gameState?: ViewerGameState;
}
export declare const ColonySprite: FC<ColonySpriteProps>;
export {};
