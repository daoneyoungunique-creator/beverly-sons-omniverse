export type RevenueSource = "stripe" | "affiliate" | "adsense";
export type VerifiedEvent = { providerEventId:string; source:RevenueSource; amountMinor:number; currency:string; verified:boolean; occurredAt:string; kind:"payment"|"commission"|"ad_report"|"refund" };
export function recognizeRevenue(event:VerifiedEvent) {
  if(!event.verified) throw Error("Unverified event must not enter actual revenue ledger");
  if(!event.providerEventId || !Number.isSafeInteger(event.amountMinor) || event.amountMinor<0 || !/^[A-Z]{3}$/.test(event.currency)) throw Error("Invalid financial event");
  return { ...event, signedAmountMinor:event.kind==="refund"?-event.amountMinor:event.amountMinor, idempotencyKey:`${event.source}:${event.providerEventId}` };
}
// Persistence must enforce UNIQUE(source, provider_event_id) and verify provider signatures server-side.
