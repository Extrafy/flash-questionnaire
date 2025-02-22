import service from "../../http/request";

export function loginapi(data) {
  return service.request({
    url: "api/qs/user/login",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function getVerificationCodeapi(data) {
  return service.request({
    url: "api/qs/user/register",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function signUpapi(data) {
  return service.request({
    url: "api/qs/user/confirm/email",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

// import { login } from '../../api/account/login'
