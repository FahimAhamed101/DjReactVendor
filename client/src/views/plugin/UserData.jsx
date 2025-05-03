import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";

function UserData() {
  try {
    const access_token = Cookies.get("access_token");
    const refresh_token = Cookies.get("refresh_token");

    // Return null if no tokens exist
    if (!access_token && !refresh_token) {
      return null;
    }

    // Try to decode the access token first, fall back to refresh token
    const tokenToDecode = access_token || refresh_token;
    
    if (!tokenToDecode) {
      return null;
    }

    const decoded = jwtDecode(tokenToDecode);
    return decoded;
    
  } catch (error) {
    console.error("Error decoding token:", error);
    // Clear invalid tokens
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    return null;
  }
}

export default UserData;