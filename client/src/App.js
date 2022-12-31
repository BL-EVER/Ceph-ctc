import Home from "./Views/Home";
import {OidcSecure, useOidc, useOidcIdToken, useOidcUser} from "@axa-fr/react-oidc";
import {AppBar, Box, Button, IconButton, Toolbar, Typography} from "@mui/material";

function App() {
    const { login, logout, isAuthenticated} = useOidc();
    const{ idToken, idTokenPayload } = useOidcIdToken();
    const {oidcUser, oidcUserLoadingState} = useOidcUser();
  return (
    <div>
        <AppBar position="static" color="primary" sx={{ bottom: 'auto', top: 0 }} style={{marginBottom: "20px"}} >
            <Toolbar>
                <img src="https://ctc-project.eu/wp-content/uploads/2021/11/cropped-CtC-Logo-Vert-Gradient.png" alt="CtC Logo" height="50"/>
                {!isAuthenticated && <Button color="inherit" style={{marginLeft: "auto"}} onClick={() => login('/')}>Login</Button>}
                {isAuthenticated && <Button color="inherit" style={{marginLeft: "auto"}} onClick={() => logout()}>logout</Button>}
            </Toolbar>
        </AppBar>
        <OidcSecure>
            <Home/>
        </OidcSecure>

        <div style={{marginBottom: "75px"}}/>
        <AppBar position="static" color="primary" sx={{ top: 'auto', bottom: 0 }} style={{marginTop: "20px"}} >
            <Toolbar>
                <Typography variant="body1" color="inherit" component="div" style={{marginLeft: "auto"}}>
                    <a href="https://ctc-project.eu" style={{textDecoration: 'underline', color: 'white'}}>© CutTheCord Project</a>
                </Typography>
            </Toolbar>
        </AppBar>
    </div>
  );
}

export default App;
/*
* {idTokenPayload != null && <p className="card-text">{JSON.stringify(idTokenPayload)}</p>}
        <p className="card-text">{JSON.stringify(oidcUser)}</p>
* */
