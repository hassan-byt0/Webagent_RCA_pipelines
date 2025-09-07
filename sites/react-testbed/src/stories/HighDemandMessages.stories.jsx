// src/components/CartReservationTimer.stories.jsx

import CartReservationTimer from './HighDemandMessages';

export default {
  title: 'Components/HighDemandMessages',
  component: CartReservationTimer,
};

/**
 * Minimal CSF: automatically shows the default story
 */
export const Default = {
  args: {
    initialMinutes: 5,
    initialSeconds: 30,
  },
};
