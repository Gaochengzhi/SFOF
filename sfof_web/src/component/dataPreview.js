import { useState } from 'react';
import { LoadingOutlined } from '@ant-design/icons';
export function DataPreview({
    isLoading, previewList, isVisible
}) {
    const [showHeaders, setShowHeaders] = useState(true);
    function handleSend() {
        fetch('http://124.220.179.145:5000/data')
            .then(response => response.blob())
            .then(blob => {
                // Create a temporary URL for the ZIP archive
                const url = URL.createObjectURL(blob);
                // Create a link element and click it to download the ZIP archive
                const link = document.createElement('a');
                link.href = url;
                link.download = 'data.zip';
                link.click();
                // Wait for the ZIP archive to finish downloading
                link.addEventListener('load', () => {
                    // Extract the files from the ZIP archive
                    JSZip.loadAsync(blob).then(zip => {
                        const csvFile = zip.file('filtered_data.csv');
                        const pdfFile = zip.file('Data Screening Technical Report.pdf');
                        // Use the FileReader API to read the contents of the files
                        csvFile.async('text').then(csv => console.log(csv));
                        pdfFile.async('arraybuffer').then(pdf => console.log(pdf));
                    });
                });
            });
    }
    return <div>
        <div className={`${isLoading ? "" : "hidden"}`}>
            <LoadingOutlined className='text-4xl' />
        </div>
        <div className={`${isLoading ? "hidden" : ""}`}>
            {/* <LoadingOutlined className='text-4xl' /> */}
            <div className='p-2 bg-green-500 text-white rounded-md shadow-md border' onClick={handleSend} >download file</div>
        </div>
    </div>;
}
