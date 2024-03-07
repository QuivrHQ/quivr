/* eslint-disable */
export const APP_ID = process.env.NEXT_PUBLIC_INTERCOM_APP_ID;

// prettier-ignore
export const load = (): void => {
    (function(){const w=window;const ic=(w as any).Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',(w as any).intercomSettings);}else{const d=document;const i=function(){i.c(arguments);};i.q=[] as any[];i.c=function(args: any){i.q.push(args);};(w as any).Intercom=i;const l=function(){const s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/' + APP_ID;const x=d.getElementsByTagName('script')[0];x.parentNode?.insertBefore(s, x);};if(document.readyState==='complete'){l();}else if((w as any).attachEvent){(window as any).attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})();
}

// Initializes Intercom
export const boot = (email: string): void => {
  (window as any).Intercom &&
    (window as any).Intercom("boot", { app_id: APP_ID, email });
};

export const update = (): void => {
  window && (window as any).Intercom && (window as any).Intercom("update");
};
