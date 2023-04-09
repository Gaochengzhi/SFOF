import React from "react";
import { FileTextOutlined } from '@ant-design/icons'
export function SelectFile({
    active,
    selectedFile,
    handleFileInput,
    handleUpload,
    selectedFile2
}) {
    return <div className='bg-gray-300 shadow-md border border-gray-400 rounded-md w-full flex justify-between'>
        <div className='text-3xl p-2'>Step 1: Choose your data set</div>
        <div className='flex items-center px-3'>
            <div className={`${active ? "" : "hidden"}`}>
                <div className='flex h-full items-center'>
                    <input id="file" type="file" value={selectedFile} onChange={handleFileInput} />
                    <button className='bg-slate-100 rounded-lg px-2 py-1 border-gray-600 shadow-sm' onClick={handleUpload}>Upload</button>
                </div>
            </div>

            <div className={`${active ? "hidden" : ""}`}>
                <button className="px-2 py-1 bg-slate-200 rounded-md shadow-sm border flex items-center">
                    <FileTextOutlined />
                    <div className="mx-2">
                        {selectedFile2}
                    </div>
                </button>
            </div>
            <div className='mx-4'>or</div>
            <div>
                <button className='bg-blue-500 text-white rounded-lg px-2 py-1 border-gray-600 shadow-md' onClick={handleUpload}>Example File</button>
            </div>
        </div>
    </div >;
}
