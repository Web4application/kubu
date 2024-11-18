// ./app/page.tsx
import ClientComponent from "@/components/ClientComponent";
import { fetchAccessToken } from "hume";

export default async function Page() {
  const accessToken = await fetchAccessToken({
    apiKey: String(process.env.h5RJsbByxogjY8C6jQLYyjabJF13ysthzioYl3cHEaZeGRD1),
    secretKey: String(process.env.f7Vm67jXcsS9IswCGAfvTbJ1frjI6ZkajMQ6aPhry0meZnryl078nLcGjG5VhSV4),
  });

  if (!accessToken) {
    throw new Error();
  }

  return <ClientComponent accessToken={accessToken} />;
}
