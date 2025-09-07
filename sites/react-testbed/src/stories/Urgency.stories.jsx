// src/components/FlashSaleTimer.stories.jsx

import FlashSaleTimer from './Urgency';

export default {
  title: 'Components/Urgency',
  component: FlashSaleTimer,
};

export const Default = {
  args: {
    // Example: 10 minutes from now
    deadline: Date.now() + 10 * 60 * 1000,
  },
};
