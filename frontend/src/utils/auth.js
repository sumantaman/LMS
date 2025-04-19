import { userAuthStore }  from "../store/auth";
import axios  from "axios";
import jwt_decode from 'json-schema';
import Swal from 'sweetalert2'


export const login  = async(email, passord) =>{
    try {
        const {data, status} =  await axios.post(`user/token/`,{
            email,
            passord,
        });
        if(status === 200){
            setAuthUser(data.access, data.refresh);
            alert("login successfull")
        }
        return {data, error:null}
    } catch (error) {
        return {
            data : null,
            error :error.response.data || "somethinf went wrong",
        };
    }

}
export const register = async(full_name, email, passord, passord2)=>{
    try {
        const { data } = await axios.post('user/register/',{
            full_name,
            email,
            passord,
            passord2,
        });
        await login(email, passord);
        alert("s")
    } catch (error) {
        console.log(error)
    }
};