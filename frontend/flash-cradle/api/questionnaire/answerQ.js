import service from '../../http/request';

export function getQ(data) {
    return service({
        url: 'api/qs/ms_create_edit/fill_in_qn_FS',
        method: 'POST',
        data: data,
    });
}

export function postQ(data) {
    return service({
        url: 'api/qs/ms-fill-analyse/fill_in_qn_SE',
        method: 'POST',
        data: data,
    });
}