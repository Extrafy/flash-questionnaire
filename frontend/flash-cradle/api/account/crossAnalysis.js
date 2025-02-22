import service from "../../http/request";

export function getapi1(data) {
  return service.request({
    url: "api/qs/ms-fill-analyse/cross_analyse_FS",
    method: "post",
    data,
    // headers: {
    //   "Content-Type": "multipart/form-data",
    // },
  });
}

export function getapi2(data) {
  return service.request({
    url: "api/qs/ms-fill-analyse/cross_analyse_SE",
    method: "post",
    data,
    // headers: {
    //   "Content-Type": "multipart/form-data",
    // },
  });
}

// import { getapi1, getapi2  } from '../../api/account/crossAnalysis'
