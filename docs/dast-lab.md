Finding: ZAP rule 10021 identified a missing X-Content-Type-Options header on / and /welcome.
Fix: Added X-Content-Type-Options: nosniff using Flask’s after_request hook.
Evidence: All three tests passed, curl confirmed the header was present, and the new ZAP report no longer contained finding 10021.
Limitations: Other alerts remain. Resolving one finding does not prove that the entire application is secure.
