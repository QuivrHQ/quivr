// Set your APP_ID
export const APP_ID = process.env.NEXT_PUBLIC_INTERCOM_APP_ID;

// prettier-ignore
export const load = (): void => {
  (function(){const w=window;const ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',w.intercomSettings);}else{const d=document;const i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.Intercom=i;const l=function(){const s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/' + APP_ID;const x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s, x);};if(document.readyState==='complete'){l();}else if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})();
}

// Initializes Intercom
export const boot = (options = {}): void => {
  window.Intercom && window.Intercom("boot", { app_id: APP_ID, ...options });
};

export const update = (): void => {
  window && window.Intercom && window.Intercom("update");
};
