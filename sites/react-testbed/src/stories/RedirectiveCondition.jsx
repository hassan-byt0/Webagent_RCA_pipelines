// src/components/RedirectiveCondition.jsx

import React from 'react';
import { Space, Tag, Typography } from 'antd';
import { EyeOutlined } from '@ant-design/icons';

const { Text } = Typography;

/**
 * A small UI banner showing product scarcity ("Few Left")
 * and the number of recent views ("28 viewed...").
 */
const RedirectiveCondition = () => {
  return (
    <div style={{ padding: 16, background: '#fff', border: '1px solid #f0f0f0' }}>
      <Space direction="vertical">
        {/* "Few Left" tag */}
        <Tag
          color="default"
          style={{
            backgroundColor: '#fff',
            borderRadius: 4,
            color: '#000',
            fontWeight: 500,
            border: '1px solid #d9d9d9',
          }}
        >
          Few Left
        </Tag>

        {/* "28 viewed in last 24 hours" bubble */}
        <Tag
          color="default"
          style={{
            backgroundColor: '#f5f5f5',
            borderRadius: 20,
            color: '#000',
            fontWeight: 400,
            border: 'none',
            display: 'inline-flex',
            alignItems: 'center',
          }}
          icon={<EyeOutlined style={{ marginRight: 4 }} />}
        >
          <Text>28 viewed in last 24 hours</Text>
        </Tag>
      </Space>
    </div>
  );
};

export default RedirectiveCondition;
