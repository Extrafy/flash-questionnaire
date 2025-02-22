import service from '../../http/request'


export function getCode(data){
  return service.request({
      url: 'api/qs/user/find_password_back_FirstStep',
      method: 'post',
      data,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
}
export function changePw(data){
  return service.request({
      url: 'api/qs/user/find_password_back_SecondStep',
      method: 'post',
      data,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
}
