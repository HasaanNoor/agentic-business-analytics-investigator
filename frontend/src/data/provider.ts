import { dataMode } from '../config/dataMode';
import { apiDataProvider } from './apiProvider';
import { staticDataProvider } from './staticProvider';

export function selectDataProvider(mode = dataMode) {
  return mode === 'static' ? staticDataProvider : apiDataProvider;
}

export const dataProvider = selectDataProvider();
