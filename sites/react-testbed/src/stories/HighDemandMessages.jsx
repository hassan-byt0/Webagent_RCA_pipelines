// src/components/CartReservationTimer.jsx

import React, { useEffect, useState, useRef } from 'react';
import { Typography, Space, Alert } from 'antd';
import { FireOutlined } from '@ant-design/icons';

const { Text } = Typography;

/**
 * A component showing that items in the cart are in high demand
 * and counting down how many minutes/seconds remain before a reservation expires.
 */
const CartReservationTimer = ({ initialMinutes = 5, initialSeconds = 30 }) => {
  const [timeLeft, setTimeLeft] = useState({
    minutes: initialMinutes,
    seconds: initialSeconds,
  });
  const intervalRef = useRef(null);

  // Format time as MM:SS
  const formatTime = (min, sec) => {
    const mm = String(min).padStart(2, '0');
    const ss = String(sec).padStart(2, '0');
    return `${mm}:${ss}`;
  };

  useEffect(() => {
    // Decrement timer every second
    intervalRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        const { minutes, seconds } = prev;
        if (seconds > 0) {
          return { minutes, seconds: seconds - 1 };
        }
        if (seconds === 0) {
          if (minutes === 0) {
            // If timer hits 00:00, stop
            clearInterval(intervalRef.current);
            return { minutes: 0, seconds: 0 };
          }
          // Decrement minute, reset seconds to 59
          return { minutes: minutes - 1, seconds: 59 };
        }
        return prev;
      });
    }, 1000);

    // Cleanup on unmount
    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      {/* "High demand" message */}
      <Space>
        <FireOutlined style={{ color: 'orange' }} />
        <Text>Items in your cart are in high demand.</Text>
      </Space>

      {/* Reservation timer box */}
      <Alert
        message={
          <Text>
            Your order is reserved for{' '}
            <Text strong>
              {formatTime(timeLeft.minutes, timeLeft.seconds)} minutes
            </Text>
          </Text>
        }
        type="warning"
        showIcon={false}
        style={{ backgroundColor: '#fff7e6', borderColor: '#ffecb5' }}
      />
    </Space>
  );
};

export default CartReservationTimer;
