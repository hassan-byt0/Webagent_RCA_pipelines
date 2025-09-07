// src/components/FlashSaleTimer.jsx

import React, { useEffect, useState, useRef } from 'react';
import { Typography, Statistic } from 'antd';
import { RedoOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Countdown } = Statistic;

/**
 * Displays a discount tag, a live countdown (e.g., 10 minutes),
 * and a promotional message: "Act Fast to Safe up to 50%..."
 *
 * Props:
 * - deadline: a Date or timestamp for the countdown finish
 */
const FlashSaleTimer = ({ deadline }) => {
  // If no deadline is provided, default to 10 minutes from now.
  const [target] = useState(deadline || Date.now() + 10 * 60 * 1000);

  // Optionally, handle onFinish
  const onFinish = () => {
    alert('Flash sale has ended!');
  };

  return (
    <div
      style={{
        position: 'relative',
        maxWidth: 360,
        borderRadius: 16,
        background: '#fff',
        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
        padding: '24px',
        textAlign: 'center',
      }}
    >
      {/* Corner discount banner */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 80,
          height: 80,
          background: '#ff1744',
          color: '#fff',
          fontWeight: 'bold',
          transform: 'rotate(-45deg) translate(-40px, 30px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 1px 6px rgba(0,0,0,0.3)',
        }}
      >
        -50%
      </div>

      {/* Countdown Timer */}
      <div style={{ marginTop: 8, marginBottom: 8 }}>
        <Countdown
          title={
            <div>
              <Text style={{ fontSize: '0.8rem', marginRight: 16 }}>Days</Text>
              <Text style={{ fontSize: '0.8rem', marginRight: 16 }}>Hrs.</Text>
              <Text style={{ fontSize: '0.8rem', marginRight: 16 }}>Min.</Text>
              <Text style={{ fontSize: '0.8rem' }}>Sec.</Text>
            </div>
          }
          value={target}
          format="DD:HH:mm:ss"
          valueStyle={{ color: '#f5222d', fontSize: '1.8rem', fontWeight: 'bold' }}
          onFinish={onFinish}
        />
      </div>

      {/* Promo Message */}
      <Title level={4} style={{ marginTop: 16 }}>
        ACT FAST TO SAFE UP TO 50% ON YOUR NEXT ORDER WITH US!
      </Title>
    </div>
  );
};

export default FlashSaleTimer;
