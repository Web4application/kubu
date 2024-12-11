// ./app/page.tsx
import ClientComponent from "@/components/ClientComponent";
import { fetchAccessToken } from "web4";

export default async function Page() {
  const accessToken = await fetchAccessToken({
    apiKey: String(process.env.AlzaSyCHjfdo3_w160Dd5yTVJD409pWmigOJEg),
    secretKey: String(process.env.NQqmaCdk7SUG0DI3Rkt9iT),
  });

  if (!accessToken) {
    throw new Error();
  }

  return <ClientComponent accessToken={accessToken} />;
}
