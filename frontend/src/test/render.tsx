import { render } from '@testing-library/react';
import type { ReactElement } from 'react';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';

export function renderWithRouter(ui: ReactElement, route = '/') {
  window.history.pushState({}, 'Test page', route);
  return render(<BrowserRouter>{ui}</BrowserRouter>);
}

export function renderWithMemoryRouter(ui: ReactElement, route = '/') {
  return render(<MemoryRouter initialEntries={[route]}>{ui}</MemoryRouter>);
}
