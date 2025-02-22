import service from "../../http/request";

export function logoutapi() {
  return service.request({
    url: "api/qs/user/logout",
    method: "post",
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function changeUserNameAPI(data) {
  return service.request({
    url: "api/qs/user/change/username",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function changeUserEmailAPI(data) {
  return service.request({
    url: "api/qs/user/change/email_SE",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function getVerificationCodeapi(data) {
  return service.request({
    url: "api/qs/user/change/email_FS",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function uploadAvatarAPI(data) {
  return service.request({
    url: "api/qs/user/change/picture",
    method: "post",
    data,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

// import { logoutapi } from '../../api/account/usercenter'
