export type Incident={id:number;title:string;description:string;severity:string;status:string;current_state:string;created_at:string}
export type Hypothesis={id:number;rank:number;title:string;explanation:string;confidence:number;evidence_for:string[];evidence_against:string[]}
export type Audit={id:number;event_type:string;actor:string;input_json:Record<string,string>;output_json:Record<string,string>;timestamp:string}
export type Verification={id:number;test_type:string;command:string;passed:boolean;duration:number;stdout:string}
