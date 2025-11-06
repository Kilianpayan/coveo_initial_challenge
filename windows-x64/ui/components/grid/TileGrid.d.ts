import { FC, PropsWithChildren } from 'react';
import { TeamGameState } from '../../GameInterface';
import { Constants } from '../PlayZone';
export declare const TileGrid: FC<PropsWithChildren<{
    children: React.ReactNode;
    constants: Constants;
    teamGameState: TeamGameState;
}>>;
