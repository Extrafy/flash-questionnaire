import Cookie from "js-cookie";

const userId = "userId";
const userEmail = "userEmail";
const userMoney = "userMoney";
const userAvatarURL = "https://s2.loli.net/2024/05/14/goXsDLbJqTMwUka.png";
export const imgUrl = "https://flash-questionnaire-exp.oss-cn-beijing.aliyuncs.com";
export function setAnsweredQ(q, content){
  Cookie.set('q' + String(q), content);
}

export function getAnsweredQ(q){
  console.log('q'+String(q));
  return Cookie.get('q' + String(q));
}

export function setUserId(id) {
  Cookie.set(userId, id, { expires: 7 });
}

export function getUserId() {
  return Cookie.get(userId);
}

export function setUserEmail(email) {
  Cookie.set(userEmail, email, { expires: 7 });
}

export function getUserEmail() {
  return Cookie.get(userEmail);
}

export function setUserAvatarURL(url) {
  Cookie.set(userAvatarURL, url, { expires: 7 });
}

export function getUserAvatarURL() {
  return Cookie.get(userAvatarURL);
}

export function setUserMoney(money) {
  Cookie.set(userMoney, money, { expires: 7 });
}

export function getUserMoney() {
  return Cookie.get(userMoney);
}

export function removeUserId(){
  Cookie.remove(userId);
}

export function removeUserEmail(){
  Cookie.remove(userEmail);
}

export function removeUserAvatarURL(){
  Cookie.remove(userAvatarURL);
}

export function removeUserMoney(){
  Cookie.remove(userMoney);
}