import React, {useEffect, useState} from 'react';
import useWindowDimensions from "../hooks/useWindowDimensions";
import axios from "axios";
import {useOidcIdToken} from "@axa-fr/react-oidc";

const SreeIframe = (props) => {
    const [iframeSrc, setIframeUrl] = useState(props.iframeSrc);

    const { height, width } = useWindowDimensions();
    const{ idToken, idTokenPayload } = useOidcIdToken();

    const loadFrame = async (payload) => {

        const iframe = document.querySelector("iframe");
        iframe.contentWindow.postMessage(payload, "*");
        setIframeUrl(props.sree)
    }

    const configureBuckets = async () => {
        try {
            const respUser = await axios.get(`/ctcapi/api/v1/users/email/${idTokenPayload.email}`,
                {

                        auth: {
                            username: "admin",
                            password: "root"
                        },
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                            'Content-Type': 'application/json',
                        }
                });
            //console.log(respUser);
            const resp = await axios.post(`/capi/assignBuckets`, {uid: idTokenPayload.email, org: respUser.data.organization});
            //console.log(resp);
        }
        catch (e) {
            console.error(e);
        }
    }

    const fetchdata = async () => {
        let payload = {
            region: "us-east-1",
            acl: "public-read",
        }
        //Fetch Endpoint
        try {
            const responseUri = await axios.get('/capi/endpoint');
            payload.endpoint = "http://" + responseUri.data;
        } catch (error) {
            console.error(error);
        }

        //Fetch Access Keys
        try {
            const responseUser = await axios.get(`/capi/user/${idTokenPayload.email}`);
            payload.accessKeyId = responseUser.data.keys[0].access_key;
            payload.secretKeyId = responseUser.data.keys[0].secret_key;
        } catch (error) {

            //Create User if not exists
            try {
                const createUserResp = await axios.post('/capi/user', {
                    "uid": idTokenPayload.email,
                    "display_name": idTokenPayload.email,
                    "email": idTokenPayload.email,
                    "user_caps": "usage=read, write; users=read",
                    "max_buckets": 1000
                });
                payload.accessKeyId = createUserResp.data.keys[0].access_key;
                payload.secretKeyId = createUserResp.data.keys[0].secret_key;

            } catch (error) {
                console.error(error);
            }
        }
        //console.log(payload);
        //await configureBuckets();
        //loadFrame(payload);
        return payload
    }
    useEffect(() => {
        Promise.all([fetchdata(), configureBuckets()]).then((data) => {
            loadFrame(data[0]);
        })
    }, [])

    return (
        <div>
            <iframe src={iframeSrc} height={height * 0.9} width={width * 0.98} style={{border: "1px solid black", marginLeft: `${width * 0.004}px`}} title="Iframe"></iframe>
        </div>
    );
};

export default SreeIframe;
/*
 /*const payload = {
            endpoint: "http://172.24.163.163:8000",
            region: "us-east-1",
            accessKeyId: "YH2BUHU3Q6HQVW0QH30T",
            secretKeyId: "gt5c2t3TCd6i9fQQwGeHxpZ6Y3ROy8cH6ulqutNu",
            acl: "public-read",
        }*/