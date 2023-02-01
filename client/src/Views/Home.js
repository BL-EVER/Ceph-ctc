import React, {useState} from 'react';
import SreeIframe from "../components/SreeIframe";
import axios from "axios";

const Home = () => {
    const [sree, setSree] = useState("");
    const [iframeSrc, setIframeUrl] = useState("");
    const setIframe = async () => {
        try {
            const sree = await axios.get('/capi/sree');
            setIframeUrl(`http://${sree.data}/config.html`);
            setSree(`http://${sree.data}`);
        } catch (error) {
            console.error(error);
        }
    }
    React.useEffect(()=> {
        setIframe()
    }, [])
    return (
        <div>
            {sree !== "" && <SreeIframe sree={sree} iframeSrc={iframeSrc}/>}
        </div>
    );
};

export default Home;