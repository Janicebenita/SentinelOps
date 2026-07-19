export type Incident={id:number;title:string;description:string;severity:string;status:string;current_state:string;created_at:string}
export type Hypothesis={id:number;rank:number;title:string;explanation:string;confidence:number;evidence_for:string[];evidence_against:string[]}
export type Audit={id:number;event_type:string;actor:string;input_json:Record<string,string>;output_json:Record<string,string>;timestamp:string}
export type Verification={id:number;test_type:string;command:string;passed:boolean;duration:number;stdout:string}
export type Evidence={id:number;evidence_type:string;summary:string;relevance_score:number}
export type Patch={id:number;diff:string;explanation:string;risk_score:number}
export type PullRequest={id:number;status:string;branch_name:string;commit_sha:string}
export type Health={ready:boolean;backend:boolean;demo_app:boolean;database:boolean;mock_provider:boolean;seeded:boolean;sandbox_mode:string;provider_warning?:string}
