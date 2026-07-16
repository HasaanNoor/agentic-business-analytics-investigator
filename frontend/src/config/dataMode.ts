export type DataMode = 'api' | 'static';

const rawDataMode = (import.meta.env.VITE_DATA_MODE || 'api').toLowerCase();

export const dataMode: DataMode = rawDataMode === 'static' ? 'static' : 'api';
export const isStaticDataMode = dataMode === 'static';

export const demoDataBaseUrl = `${import.meta.env.BASE_URL}demo-data/`;
