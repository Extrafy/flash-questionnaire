import MobileDetect from 'mobile-detect';

export function isMobile() {
  const md = new MobileDetect(window.navigator.userAgent);
  return md.mobile() !== null;
}