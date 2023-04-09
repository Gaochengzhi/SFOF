import { useState } from 'react';
import { LoadingOutlined } from '@ant-design/icons';
export function DataPreview({
    isLoading, previewList
}) {
    const [showHeaders, setShowHeaders] = useState(true);
    return <div>
        <div className={`${isLoading ? "" : "hidden"}`}>
            <LoadingOutlined className='text-4xl' />
        </div>
        <div className={`${isLoading ? "" : ""}`}>
            {/* <LoadingOutlined className='text-4xl' /> */}
            <div className='bg-gray-500'>klcdshjl</div>
        </div>
    </div>;
}
