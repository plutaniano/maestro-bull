(async () => {
  const API_URL = "https://api.maestrocapital.com.br/xpaccount/access_token";
  const SESSION_STORAGE_KEY =
    "oidc.user:https://identity.xpi.com.br:rede.assessores";
  const {
    access_token,
    expires_at,
    profile: { account, auth_time },
  } = JSON.parse(window.sessionStorage[SESSION_STORAGE_KEY]);

  if (window.confirm("Clique em OK para enviar os cookies.")) {
    try {
      await fetch(API_URL, {
        method: "POST",
        body: JSON.stringify({
          access_token,
          expires_at,
          auth_time,
          advisor: account,
        }),
      });
      alert("Cookie adicionado com sucesso");
    } catch (e) {
      alert("Falha ao enviar cookie");
    }
  }
})();
