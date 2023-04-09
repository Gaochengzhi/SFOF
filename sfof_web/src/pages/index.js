import { DataPreview } from './../component/dataPreview';
import { Foot } from './../component/foot';
import { FilterData } from './../component/filterData';
import { Header } from './../component/header';
import { SelectFile } from '../component/selectFile';
import { useState } from 'react'
import axios from 'axios';
// import 'antd/dist/antd.css';



export default function Home() {
    const [field, setField] = useState('');
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [active, setactive] = useState(true);
    const [isLoading, setIsLoading] = useState(false)
    const [isVisible, setIsVisible] = useState(false)


    const [selectedFile, setSelectedFile] = useState("");
    const [selectedFile2, setSelectedExpFile] = useState(null);
    const [framList, setFrameList] = useState([0, 2293]);
    const [previewList, setPreviewList] = useState(["", ""])
    const handleSliderChange = (newValue) => {
        setFrameList(newValue);
    };
    const handleFileInput = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const [checkedVtItems, setCheckedVtItems] = useState({
        Car: false,
        Truck: false,
        Bus: false,
        Pedestrian: false,
        Cyclist: false,
    });
    const handleVtCheck = (event) => {
        setCheckedVtItems({
            ...checkedVtItems,
            [event.target.name]: event.target.checked,
        });
    };

    const checkboxVtElements = Object.keys(checkedVtItems).map((key) => (
        <label key={key} className='text-xl p-1'>
            <input
                type="checkbox"
                name={key}
                checked={checkedVtItems[key]}
                onChange={handleVtCheck}
                className='m-1'
            />
            {key}
        </label>
    ));

    const checkedItemsList = Object.keys(checkedVtItems)
        .filter((key) => checkedVtItems[key])
        .map((key) => <li key={key}>{key}</li>);

    async function fetchData(selectName) {
        try {
            const response = await axios.post('http://127.0.0.1:5000/filter', {
                frame_range: framList,
                selected_names: selectName,
            })
            setPreviewList(response.data.preview)
            // The filtered data will be available in response.data
            console.log(previewList);
        } catch (error) {
            console.error(error);
        }
    }


    const handleUploadFile = () => {
        setactive(false)
        setSelectedExpFile("data.json")
    };
    const handleFilterFile = () => {
        console.log(framList);
        console.log(checkedVtItems);
        const selectedVtItems = [];

        for (const item in checkedVtItems) {
            if (checkedVtItems[item]) {
                selectedVtItems.push(item);
            }
        }
        fetchData(selectedVtItems);
        setIsLoading(true)
    }
    return (
        <main className="flex min-h-screen flex-col items-center p-24 space-y-3">
            <Header />

            <SelectFile active={active} selectedFile={selectedFile} handleFileInput={handleFileInput} handleUpload={handleUploadFile} selectedFile2={selectedFile2} />

            <FilterData active={active} checkboxVtElements={checkboxVtElements} checkedItemsList={checkedItemsList} framList={framList} handleSliderChange={handleSliderChange} handleFilterFile={handleFilterFile} />
            <DataPreview isLoading={isLoading} previewList={previewList} />



            <Foot />
        </main >
    )
}
