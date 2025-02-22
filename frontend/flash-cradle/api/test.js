import service from '../http/request'

export function testFuck(data){
    return service.request({
        url: 'api/qs/user/login',
        method: 'post',
        data
      })
}
