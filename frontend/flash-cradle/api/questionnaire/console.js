import service from "../../http/request";

export function getQ(data) {
    return service({
        url: '/api/qs/info/get_survey_data',
        method: 'post',
        data,
    });
}
export function releaseQ(data) {
    return service({
        url: '/api/qs/Status/deploy_qn',
        method: 'post',
        data,
    });
}
export function pauseQ(data) {
    return service({
        url: '/api/qs/Status/pause_qn',
        method: 'post',
        data,
    });
}
export function deleteQ(data) {
    return service({
        url: '/api/qs/Status/delete_survey_not_real',
        method: 'post',
        data,
    });
}
export function copyQ(data) {
    return service({
        url: '/api/qs/ms_create_edit/copy_survey',
        method: 'post',
        data,
    });
}
export function editQ(data) {
    return service({
        url: '/api/qs/Submit/edit_survey_FS',
        method: 'post',
        data,
    });
}
export function shareQ(data) {
    return service({
        url: '/api/qs/Status/release_to_square',
        method: 'post',
        data,
    });
}




