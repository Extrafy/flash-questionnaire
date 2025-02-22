import service from '../../http/request';

export function createQ(data) {
    return service({
        url: '/api/qs/ms_create_edit/create_QN',
        method: 'post',
        data,
    });
}
export function editQFetch(data) {
    return service({
        url: '/api/qs/ms_create_edit/edit_survey_FS',
        method: 'post',
        data,
    });
}
export function editQSend(data) {
    return service({
        url: '/api/qs/ms_create_edit/edit_survey_SE',
        method: 'post',
        data,
    });
}
