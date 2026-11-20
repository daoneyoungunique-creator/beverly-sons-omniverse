export type Platform = "youtube" | "instagram" | "facebook" | "tiktok" | "linkedin" | "pinterest";
export type ContentJob = { id:string; sourceId:string; brand:string; caption:string; platforms:Platform[]; approved:boolean; rightsCleared:boolean; scheduledAt?:string };
export type PublishReceipt = { jobId:string; platform:Platform; status:"queued"|"submitted"|"confirmed"|"failed"; externalId?:string; error?:string };
export interface SocialPublisher { publish(job:ContentJob, platform:Platform):Promise<PublishReceipt> }
export function validateJob(job:ContentJob):void {
  if(!job.id || !job.sourceId || !job.brand || !job.caption.trim()) throw Error("Missing required content");
  if(!job.approved || !job.rightsCleared) throw Error("Human approval and rights clearance required");
  if(!job.platforms.length || new Set(job.platforms).size !== job.platforms.length) throw Error("Invalid platform selection");
}
export async function distributeApproved(job:ContentJob, publisher:SocialPublisher):Promise<PublishReceipt[]> {
  validateJob(job);
  const results:PublishReceipt[]=[];
  for(const platform of job.platforms) {
    try { results.push(await publisher.publish(job,platform)); }
    catch(error) { results.push({jobId:job.id,platform,status:"failed",error:error instanceof Error?error.message:"Unknown publishing failure"}); }
  }
  return results;
}
export class DraftOnlyPublisher implements SocialPublisher {
  async publish(job:ContentJob,platform:Platform):Promise<PublishReceipt> {
    return {jobId:job.id,platform,status:"queued"};
  }
}
