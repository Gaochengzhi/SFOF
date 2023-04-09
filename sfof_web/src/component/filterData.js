import React from "react";
import { Checkbox, Slider } from 'antd';
export function FilterData({
    active,
    checkboxVtElements,
    checkedItemsList,
    framList,
    handleSliderChange,
    handleFilterFile
}) {
    return <div className='bg-gray-300 shadow-md border border-gray-400 rounded-md w-full flex flex-col justify-between p-2'>
        <div className='text-3xl'>Step 2: Filter data field</div>
        <div className={`${active ? "hidden" : ""}`}>
            <div className='bg-slate-200 py-2 px-1 my-2 rounded-md flex justify-between'>
                <div>
                    <h2 className='text-xl'>Select Vehicle Types:</h2>
                    {checkboxVtElements}
                    <div className='px-2'>
                        <h3 className='font-bold'>Checked Items:</h3>
                        <ul>{checkedItemsList}</ul>
                    </div>
                </div>
                <div className='border-l-2 border-dashed px-4 border-gray-400'>
                    <h2 className='text-xl'>Select Frame Range</h2>
                    <div>
                        <h2>Select a Range:</h2>
                        <Slider range defaultValue={framList} min={0} max={2293} onChange={handleSliderChange} />
                        <div>
                            <h3>Selected Range:</h3>
                            <p>{framList[0]} to {framList[1]}</p>
                        </div>
                    </div>
                </div>
                <div className='flex flex-col items-end justify-end'>
                    <button className='bg-blue-500 text-white py-1 px-2 rounded-md shadow-md mx-2' onClick={handleFilterFile}>
                        Submit
                    </button>
                </div>
            </div>
        </div>
    </div>;
}
