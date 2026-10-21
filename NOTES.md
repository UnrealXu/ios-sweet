# iOS 16 on sweet (Redmi Note 10 Pro, SM7150) - working notes

## ACTIVE HANDOFF: computer transfer snapshot (2026-10-21)

- Published snapshot e7a697de1edb63c065f03a5d5820f93f2cd71d73; fetched
  remote tree5baff89bc870e14cd7343ecd729f9881b0552111 exactly matches
  local d3a6d76889f470432f6cef98c25ad522957aec61 source tree.
- User requested Git upload for continuing on another computer; physical experiments
  stopped. Source baseline5e5f7cd; transfer branch codex/ace-handoff-20261021 in
  UnrealXu/ios-sweet. See handoff/20261021/README.md for clone and resume steps.
- Last physical observation: retained1711085c34...944c fullreadback verified,
  diagnostic controller64843 TERMINALrc0, firmwareFastboot verified, allhandles
  terminal. No new phone operation for migration. Objective UNACHIEVED.
- Private research/inputs/backups/transport/evidence remain OUTSIDE Git. Transfer
  research/ privately preserving paths; local inventory/analysis under
  research/ace-git-handoff-20261021. Fresh clone alone cannot resume phone trials.
- Added review-only probe diagnostic proposal; caller return-chain remains PRIVATE
  WIP, unintegrated. EarlyFastboot detector already integrated; future paired gate
  needs new terminal-phase handling and fresh independent physical verification.
- Publication uses a snapshot on existing remote kernel lineage, preserving current
  source tree without uploading ignored artifacts or local experimental history.


## ACTIVE HANDOFF: CEforensic1711 fullreadback; currentnativegap; earlyFB integrated (2026-10-21)

- Forensic64843 TERMINALrc0 ADB28.1s/currenta086/rootB/FULLboot1711085c34bcb4c399ac67e08885b5f13e6327a8e9d418d259bcd1bd659d944c
  +vendor/logs/AEE/strictreturn/physicalfirmwareFastboot verified. RETAIN1711
  FULLreadback, allphonehandlesTERMINAL. ScreenshotINSPECTED Androidbootanimation
  only, notXNU/iOSdisplay. Manualhelpfulfilled/no pendinghumanquestion.
- Actuald459 pmsg19836B SHA23fb72fd421897a3e17bc43485ab29c15c2dd5fb957bedfcbc419d4cfd94a357:
  1armed/1XNUentry/rootfail, ZEROACECE1/ACERAMERR/RAMmarker. CurrentuniqueAEE02
  SHA48d542687009f97e6e67a68eddeb64a0349e189e5ed7ac6da68f3493091d4561,
  55CRC/sizePASS/byteexactpmsg. PCfffffe0007794b04=_bsd_init+8e4 rootfailWFE,
  WDT38.153282. Historical03ba9f...isold0a91-8/2.066s, explicitlyEXCLUDED.
  No currentsecond-native/probe/CEpermissionproof. Findingsaee-analysis/final.
- Realrawring replay67edfe73...a91=start=size19836/free45688/pending1/FIRST0/
  uniqueorder/prefixeligible. Counterfactualsupportedstub gateappend92B PASS,
  notactualprobeobservation. Needreturnchainbeforeprobe/newnormalrefusaltrace.
- PRIVATEbounded+ramagentsimplementminimalownedonceS4returnentry/S5selection/
  refusalprepare/beforeprobeintent +rawEL/DAIF/ISAR0/CPACR sentinel/preciserc;
  no feature/record/MMU/reset changes. Native/sharedCEsourceunchangedpendingpatch.
- IntegratedprivateearlyFB b8d22de...5ee afterforensiccomplete: rescueonly actual
  departure+>=10s+expectedserialphysical4fields/freshADBabsent → specifiedearly
  terminalfailure, no reboot/write. Parent23autotestsPASS/private11timelinecases
  PASS. Futurepairedgate mustacceptnewphasewithterminal+NEW independentFB proof.
- No userdata/GPT/protected/slotwrite. Humanresumedwork; objectiveUNACHIEVED.

## ACTIVE HANDOFF: CEforensic1711 installed; readoutLIVE afterhumanresume (2026-10-21)

- Writer5286 TERMINALrc0 one64MiBboot_b ACK Sending1.385s/Writing0.143s/
  total1.531s. INSTALLED1711085c34bcb4c399ac67e08885b5f13e6327a8e9d418d259bcd1bd659d944c,
  tokena086a91d6bcec01f/priord4599ec9883a7f6d, ACKONLY/lastFULL9e7b. RETAIN.
- Wrapper/controller64843 LIVE USBobserverreadybeforeboot, private
  ace-ram-ce-forensic-20261021/phone-trial. PollSAME64843 NEVERrestartconsumed
  writer/controller. Needcurrenttoken/rootB/fullboot/vendor/pstoreCEtrace/AEE/
  screenshotinspection/strictADBreturn/physicalfirmwareFastboot. NoXNU/no seed/
  noCE/norescue inforensic; diagnosticnotgoalcompletion. Humanmanualhelpfulfilled.
- Sourcefrozenb573c77; no userdata/GPT/protected/slotwrite. Goalunachieved.

## ACTIVE HANDOFF: humanresumed/manualFastboot verified; CEforensic1711 ready (2026-10-21)

- USERconfirmed manualFastboot/restoredconnection andrequestscontinue. Fresh
  serial-boundproduct/B/unlocked/is-userspaceno allrc0; newmanualattribution
  appendedprimary extended-readonly-usb.json andmanual-recovery-verified.json.
  Workresumedonhumaninstruction; goaltoollastsnapshotstillblocked(usercontrolled).
- Conditionalpackage87029 TERMINALrc0 actualfailed540s+newphysicalFastboot/
  sourcefreeze/5QEMU/fullring/exact64MiB/backup/adb4ACK+9e7bFULLancestryPASS.
  Freshforensiccandidate1711085c34bcb4c399ac67e08885b5f13e6327a8e9d418d259bcd1bd659d944c,
  tokena086a91d6bcec01f/priord4599ec9883a7f6d, noXNU/no seed/noCE/noRAMrescue,
  originalgeneric/pinnedAndroid/samepreviouslyapprovedforensicexception.
- Nextoneguardedwrite+freshreadout; no1711writeyetatcheckpoint. NeedactualCE
  CPUtrace/PC/AEE beforefix. Sourcefrozenb573c77 untilreadoutcomplete.
- No userdata/GPT/protected/slotwrite. ObjectiveUNACHIEVED; no iOSsuccessclaim.

## ACTIVE HANDOFF: goal BLOCKED awaiting manual Fastboot (2026-10-21 10:13UTC)

- Fresh10:13:20UTC serial-boundUSB check: fastboot/ADB bothrc0/noexpectedphone.
  Same lostcontrol/manualinput blocker persists originalgoalturn+2consecutive
  automaticcontinuations; precedingcontinuationNOprogress, no livehandle wait.
  Blockedauditmet; update_goal returnedstatusBLOCKED. ObjectiveUNACHIEVED.
- No furtherautomaticpoll/write/reboot whilewaiting. HumanmanualFastboot reply
  oractualexternaltransportchange required. Preserveadb4ACKONLY/lastFULL9e7b/
  alloriginalbackups, sourcefrozenb573c77, pairedCEprebuilt29365/noledger.
- Resume: identity-boundphysicalFastboot4fields+actualmanualattribution→append
  freshobservation→gatedpairpackage/review/onewrite/onefreshreadout→actualCE/AEE
  analysis. Neverrestartoldwriter/controller. No userdata/GPT/protected/slotwrite.

## ACTIVE HANDOFF: continuation USB recheck still absent (2026-10-21 10:11UTC)

- Previousgoalturn madecode/physicalevidenceprogress; thiscontinuation only
  revalidates sameexternalblocker, NOTverifiedwait(no livephoneprocess).
  Freshserial-boundfastboot+ADB inventory bothrc0/noexpectedphone; private
  phone-trial/continuation-usb-observations.json retains10:11:05UTC result.
- ManualFastbootquestionstillpending/nohumanresponse. Allpriorhandlesterminal;
  no writer/controllerrestart/newphoneoperation. Keep sourcefrozen/adb4ACKONLY
  retained/lastFULL9e7b andprebuiltforensic gated. GoalACTIVE, blocked threshold
  notyetmet; needexternalconnectionchangebeforeactuallogreadoutcancontinue.

## ACTIVE HANDOFF: CE lostUSB confirmed; awaitingmanualFastboot (2026-10-21)

- Controller70622 TERMINALrc1 noADB540s; extendedREADONLYobserver26717
  TERMINALrc0 afteradditional180s/19observations noexpectedADB/Fastboot. All
  phonehandlesTERMINAL. MANUALFastbootquestionpending, nohumanreplyyet.
  INSTALLEDadb4ec2ef7de485f0729348555cc05d451ac2587b3cb9f219e6de251e974867a
  token d4599ec9883a7f6d ACKONLY; lastFULL9e7b. RETAIN; no rollback/retry.
- OncehumanreturnsFastboot: freshserial-bound4getvars +manualattribution, retain
  newobservation in primaryextended-readonly-usb.json (oldfactsunchanged), then
  andONLYthen ace-ram-ce-forensic-20261021/package-reviewed.py (prebuild29365
  rc0)→review→write-forensic-once.py ONCE→run-forensic-once.py ONCE. Tokena086...
  prior d459..., noXNU/no seed/noCE/norescue; inspectactualCPUtrace/AEE beforefix.
  Neverrestartconsumed70622/writer89213 orcallCEsuccesswithoutactualevidence.
- RuntimeKEEPFROZEN b573c77 forprebuiltpairedforensic. LaterPRIVATEready:
  ace-early-fastboot-failure-20261021/early-fastboot-auto.PROPOSAL.patch
  SHAb8d22de845b4f3eef3bc4b5a68f6d947f7d98fa76054f5b2c04e5012e3a3b5ee,
  11testsPASS. IntegrateONLYafterforensicreadout; newpairgateexample alsoready.
  This avoidswaitONLYifactualphysicalFastbootreturns, notlostUSBfix.
- Private ace-terminal-handoff-mode-20261021/terminal-mode.diff94d68d29...cc10
  +ace-rootwriter-park-handoff-20261021 ready/tested, notintegrated/physicalproof.
  No userdata/GPT/protected/slotwrite. GoalACTIVE/unachieved; awaitingmanualinput.

## ACTIVE HANDOFF: guardedCE adb4 failed540s; USBabsent/manualhelp pending (2026-10-21)

- Controller70622 TERMINALrc1 after540s noADB, writer89213consumedrc0.
  INSTALLEDadb4ec2ef7de485f0729348555cc05d451ac2587b3cb9f219e6de251e974867a
  ACKONLY/lastFULL9e7b. No currentCEtrace/pstore/record recovered yet; cannot
  claimCEpermission/hashprogress/RAMboot. RETAINadb4; no blindretry/restore.
- Independentreadonlyobserver26717 LIVE up to180s, firstexpectedFastboot/ADB
  absent. PollSAME26717. After540s+readonlyverifiedlostchannel manualFastboot
  assistance requestedperAGENTSlastresort; awaitinghuman. No manualresponseyet.
- PairedCE29365 prebuilt5QEMU/fullringPASS sourcefrozenb573c77. NOcandidate/
  ledger/package/write yet; actualpostfailure firmwareFastboot requiredbefore
  package-reviewed.py. SourceKEEPFROZENuntilpairedforensicreadoutcomplete.
- PRIVATEearlyFastbootfailure detector testsPASS, notintegrated; onlyfuture
  confirmedfirmwareFastbootreturnavoids540swait, cannotfixabsentUSBcontrol.
  No userdata/GPT/protected/slotwrite. GoalACTIVE, no actualiOSusability.

## ACTIVE HANDOFF: guardedCE adb4 installed; automatic physical trial LIVE (2026-10-21)

- Localb573c77 integrates7fileCE. Writer89213 TERMINALrc0 one64MiBboot_b ACK
  Sending1.387s/Writing0.136s/total1.525s. INSTALLED
  adb4ec2ef7de485f0729348555cc05d451ac2587b3cb9f219e6de251e974867a,
  tokend4599ec9883a7f6d, ACKONLYpendingreadback/lastFULL9e7b. RETAIN.
- Wrapper/controller70622 LIVE USBobserverreadybeforeboot, private
  ace-ram-ce-20261021/phone-trial. PollSAME70622 NEVERrestartconsumedwriter/
  controller. Up to540s; needactualCECPUtrace/nativeprogress/RAMno_data/rootB/
  currenttoken/fullbootvendor/logs/screenshot/strictreturn/physicalFastboot.
  CEpermissionandperformance NOTyetphysicalverified; no successclaim.
- Sharedruntimefrozenb573c77. Paired29365 TERMINALrc0 5QEMU+fullringPASS,
  ace-ram-ce-forensic-20261021/PREBUILD_READY.json. Nofullcandidate/ledger/
  phonewrite; packageONLYactualprimary540sfailure+actualpostfailureFastboot.
- No userdata/GPT/protected/slotwrite; no manualactionpending. GoalACTIVE;
  actualiOSnotyetusable. Privatehandoff/guardpark/rootwriter remainundeployed.

## ACTIVE HANDOFF: guarded native CE candidateadb4 ready; write NEXT (2026-10-21)

- Integratedreviewed7filepatch ec3fdf3b078c6ebf819aed4b1eaed1f41caed322aa44f53639e69384f77311c1:
  CE onlyRAMrescueprofile/codecdefine; externalguard+core+strictalignedworker,
  allCgeneralregs/strictalign. Fullhash/tails/scalarfallback/software120s/150s
  guard/controller540s unchanged. No cache/MMU/VBAR/recordABI/bootreason changes.
- FreshliveCPUprobe SHA2field1/2/EL1/DAIF beforeCPACR read; observedISAR0/CPACR
  once92BACECE1 currenttoken F/R separately ownednonwrappedring, exactappend
  confirmation beforeallow; freshsamephaseprefix/STOP refused, cachedsameImage
  Rcommit retainsCEafterSTOPconsumed for2ndhash. TraceNOTpermissionproof.
- Agent12gatecases/on+offwhole-nativecompile/link+newsourceactualEL1QEMU full
  Q/FPCR/FPSR/CPACR/VBARrestore/unaligned/codec/fallbackPASS; parent8initrdtests/
  source7hashmatch/diffcheckPASS. Independentfinalreview no blocking.
- Freshbuild61563 TERMINALrc0 sameaccepted0118/profile3 candidate
  adb4ec2ef7de485f0729348555cc05d451ac2587b3cb9f219e6de251e974867a,
  tokend4599ec9883a7f6d;3entry+Centry/exact6guard63700PASS; offlineprepare47995
  full9e7bancestry/backups/freshtokenabsence/source/artifact/contractsPASS,
  freshguardedwriter/controller. Nextonewrite, noadb4writeyetatcheckpoint.
- PairedCE29365 offlineprebuildLIVE/no package/candidate/ledger; packageonly
  actual540sfailure+actualpostfailureFastboot. Phone9e7bFULLverifiedFastboot.
- Rootwriterterminal-mode private94d68d29...cc10 nowimplemented/tested with
  155sstable/realparentSIDexitproof, NOTintegrated/notphysicalRAMvalidated.
  No userdata/GPT/protected/slotwrite. GoalACTIVE/no iOSsuccessclaim.

## ACTIVE HANDOFF: real watchdog interrupted software SHA; CE integration private (2026-10-21)

- Actual2ae6... AEE unique db.fatal.01.HWT.dbg SHA
  1e7f6464abfe457e49181645ffbcbe8046b1fe7b2b4e3cd95da6ddf7abeb109d,
  55CRC/sizePASS. TFA38.160392 watchdog;39.162191 CPU0PC40005468/SP4460fc50,
  exact8aa3 ELFf9c4917f482483e82ae579ea9cc8c0386bc2a774dac9e897ae0a5f0680349b9f:
  ace_sha_block5320+148 EOR compressionround. NOTnativehalt/Android/RAMLinux;
  LR is SHA initialh1, notreturnaddress. ESR_EL2 SMC residual notEOR_EL1fault.
  AEEpmsg==Androidpmsgbyteexact19836B. Evidenceaee-analysis/findings.md.
- Establishedblocker HARDWAREwatchdog~38s beatsfullscalarhash, NOT120ssoftware
  gatepassed. DoNOTexpandbudgetagain/skiphash/guessfeedregisters. Nextfeature-
  gated SHA2CE optimization fromprivateEL1-testedstaging1 preservesfullhash,
  allQ/FPCR/FPSR/CPACR/VBAR normalreturn, alignedstaging, generalregsC+strictalign
  worker. LiveEL2/3permission remainsunknown; existingexception/AEEdiagnose.
- ram_recovery PRIVATEwhole-nativeintegration/profilemanifest/ownedCPUtrace;
  bounded_root_failure independentreview. TracephaseF/R eachonce/currenttoken,
  freshsamephaseprefixrefuse; cachedallowonlysameImage letsconsumedRESCUEcommit
  secondhashstillCE; freshSTOPrefuses. TraceBEFOREFPEN/SIMD, appendfailnoCE,
  noVBar/MMU/cache/recordABIchange. No sharedchangesyet/no newphonewrite.
- Phone9e7b FULLverified retainedFastboot/allphonehandlesTERMINAL. Usermanual
  restoredpriorloop, photoOrangeState notfailurecauseproof. GoalACTIVE.
- No userdata/GPT/protected/slotwrite. Rootwriterterminalhandoffmodeprivateonly.

## ACTIVE HANDOFF: paired9e7b fullreadback; new120s failure under analysis (2026-10-21)

- Writer14473 TERMINALrc0 one64MiBboot_b ACK Sending1.385s/Writing0.167s/
  total1.553s; forensic57746 TERMINALrc0 ADB30.1s/current47e5e2356fa3fd73/
  rootB/FULLboot9e7beb8b0f6a9f77af7a6b347655261a59d029589ecb93b76a5b35e4258c5d21
  +vendor/logs/AEE/strictreturn/physicalfirmwareFastboot verified. RETAIN9e7b
  FULLreadback, allphonehandlesTERMINAL. diagnostic_only_return_verified true,
  automatic_loop falseintentional. ScreenshotINSPECTED Androidbootanimation only.
- Actualprior2ae6... pmsg19836B SHA0fbb8b829b0685a249c60562c9c10bb6961a8d4fce21cadce08b454dd7d4b33a:
  1armed+1XNUentry+BSDmountfail, ZERO ACERAMERR/ACEANDROID/ACERESCUE/ACE_RAMDIAG/
  ACEFALL1/ACEFBREQ. AbsencealoneNOTproofpreparepassed/Androidjump/RAMsuccess.
  Private pmsg-throughput120.bin. Userphoto/repeatinglogo+manualFastboot kept
  truthfullyprivate; no autoFastbootclaim.
- ram_recovery doingactualtoken-boundAEECRC+exact8aa3ELFPC/LR/SP/ESRdecode;
  bounded_root_failure reviewingremaininguntracednativeFDTcopy/handoff/refusal
  paths. Needactualnextcode beforefix; sharedruntimeunchanged79fa857.
- Private rootwriter155sstable/pidfdreceipts proposalready butcontrollerterminal
  handoffmissing; agentnowPRIVATE implementingmode+wrapperproof, no deployment.
  No userdata/GPT/protected/slotwrite. GoalACTIVE, actualiOSnotyetusable.

## ACTIVE HANDOFF: throughput120 failed540s/user bootloop; paired9e7b ready (2026-10-21)

- Controller72759 TERMINALrc1 noADB540s, 8aa3 ACKONLY/lastFULLecdb. Independent
  readonly09:18:09UTC physicalfirmwareFastboot/productB/unlocked allrc0. USER
  thenexplicitlyreports repeatingOnePluslogo/black/restart andmanualFastboot:
  attributeFastboottoUSERmanual, exacttimingunknown, NEVERautomaticreturnsuccess.
  UserIMG_4843 inspectedOnePlus/OrangeState unlockedbootloaderprompt; noXNU/iOS/
  RAMvisibleproof. Privatephoto+manualreport ace-ram-throughput120-forensic-20261021.
- Conditionalpackage91204 TERMINALrc0 actualterminal540sfailure+realFastboot/
  sourcefreeze/5QEMU/fullringpreservation/exact64MiB/backup/8aa3ACK+ecdbFULLwith
  strictcompletionancestryPASS. Pairedcandidate
  9e7beb8b0f6a9f77af7a6b347655261a59d029589ecb93b76a5b35e4258c5d21,
  token47e5e2356fa3fd73/prior2ae6f34a318326c4; noXNU/no seed/noRAMrescue,
  originalgeneric/pinnedAndroid, previouslyapprovedforensicexception.
- Nextoneguardedwrite/readout, no9e7bwriteyetatcheckpoint. Needactualcurrent
  nativehashprogress/AEE/RAM traces; doNOTinferfailurefromlogo. No userdata/
  GPT/protected/slotwrite. GoalACTIVE, no actualiOSusability.

## ACTIVE HANDOFF: throughput120 8aa3 installed; automatic physical trial LIVE (2026-10-21)

- Writer21374 TERMINALrc0 one64MiBboot_b ACK Sending1.432s/Writing0.151s/
  total1.585s. INSTALLED8aa303985e59c627b3c7d9fc38f9c3879f6cca90fba9e8f069ea988dcbb4e49d,
  token2ae6f34a318326c4, ACKONLYpendingfullreadback/lastFULLecdb. RETAIN.
- Wrapper/controller72759 LIVE USBobserverreadybeforeboot, private
  ace-ram-throughput120-20261021/phone-trial. PollSAME72759 NEVERrestartconsumed
  writer/controller. Explicitrescuedeadline540s, productionnative120s basedactual
  throughput/150sRAMguard. NeedactualRAM/no_data/currenttoken/rootB/fullboot/
  vendor/logs/screenshot/strictADBreturn/physicalfirmwareFastboot. No successclaim.
- Sharedruntimefrozen79fa857. Paired33780 TERMINALrc0 native+5QEMU/fullring
  preservation PASS; private ace-ram-throughput120-forensic-20261021, nofull
  candidate/ledger/write. PackagingONLYactualprimary540sfailure+lateractualFB.
- PrivateCE/nativeFastbootreason proposalsNOTintegrated. Private rootwriter
  realguardreceipt/handoffintegration ongoing, neverexecbeforeactualRAM/no_data/
  stable>150sproof. No userdata/GPT/protected/slotwrite. GoalACTIVE.

## ACTIVE HANDOFF: throughput120 8aa3 ready; guarded write NEXT (2026-10-21)

- Local79fa857 measuredbudget/readretryfix. Build78981 TERMINALrc0 candidate
  8aa303985e59c627b3c7d9fc38f9c3879f6cca90fba9e8f069ea988dcbb4e49d,
  token2ae6f34a318326c4 sameaccepted0118/profile3/scalar/progress120s+guard150s,
  controller540s. Fresh3entry+Centry/exact6guard73272PASS.
- Offlineprepare19303 TERMINALrc0 FULLactualecdb/rootB/vendor/strictreturn+
  reviewedterminalcompletion/backups/newtokenabsence/currentallsource/artifacts/
  contractsPASS. Freshonewriter/controller, nextonewrite. No newphonewriteyet.
- Paired33780 prebuildLIVE frozen79fa857 runtime; nocandidate/ledger/write.
  Conditionalactualprimary540sfailure+actualFastboot requiredbeforepackage.
- Phoneecdb FULLverifiedFastboot retained. No userdata/GPT/protected/slotwrite.
  GoalACTIVE, no iOSusability/display/touchclaim.

## ACTIVE HANDOFF: measured120s + bounded return fix integrated; building (2026-10-21)

- Productionnative budget120s/1560000000ticks basedactual1.2717MiB/s and~73s
  two fullhashpasses; stillbounded/fullhash+two-pass/latchunchanged. Explicit
  rescuecontrollerdeadline540=120prepare+150RAMguard+120rescue+150Androidmargin;
  normalRAM240/Android150 unchanged. NoCE/noFastbootreason feature integrated.
- Integratedprivate ce4ece91...6f3f twofilepatch: absenttransport savedemptyread,
  global<=3includingeachrefreshedreturn, <=2one-secondreadpauses, completeother
  immediatelystops. Historical ecdb completionacceptance strictreceipt/helper/
  originalcontroller/logSHA allowlist, fullancestry gates andfailedlaunchrc1
  preserved; notgeneralrc1exception. Agentactualprior+forgeryrefusalPASS.
  Parent23auto+4rescuereadouttestsPASS/pycompile/diffcheckPASS.
- Freshbuild78981 LIVE ace-ram-throughput120-20261021 token2ae6f34a318326c4,
  sourcecompiledsameaccepted0118/profile3, explicitpriorFULLECDB+strictcompletion.
  Next3entry+Centry/exact6guard/prepare thenonewrite/controller. NOnewwriteyet.
  Phoneecdb FULLreadback firmwareFastboot retained/allphonehandlesTERMINAL.
- Paired47e5e2356fa3fd73 privateadaptedtoactual540s failure+strictcompletedancestor;
  8negativeancestrycasesPASS, no nativebuild/candidate/ledger untilactualmain
  BUILD_COMPLETE/sourcefreeze. Neverpackagebeforeactualfailure+Fastboot.
- Actualscalarpmsg19976B SHAc88967a8814dca4f0f8c05044bb8b7d86742b9d88ea9fb33d8543ff851bdac70.
  No userdata/GPT/protected/slotwrite; goalACTIVE, actualiOSnotyetusable.

## ACTIVE HANDOFF: ecdb fullreadback; bounded return completion; actual hash throughput (2026-10-21)

- Forensic48892 TERMINALrc1 afterADB28.1s/fullbootecdb+vendor/rootB/logs/AEE:
  firstreturnrecord readempty; nextidentitylookupabsent causedimmediateabort.
  Originalcontroller-launch remainsrc1 andunchanged. Subsequentreadonlyfound
  expectedADB again; NEVER restartedtrial/controller. Private complete-return-once.py
  verifiesexactfailure/fullreadback/artifacts/currentmanifest, usesremaining<=3
  totalreads, oneADBreturn, physicalfirmwareFastboot. Helper53566 TERMINALrc0:
  2totalrecordobservations(oneempty+onematching),1returnreboot, Fastbootverified.
  Receipt return-completion.json pinsoriginal+finalidenticallaunch9493157a...8853,
  source645dd91c...11bb. State explicitreturn_completion_verified=true.
  RETAINecdb9763fdf5ed6edf658cb5bb61f964ffacf760d96669f14186850250c3f5e5 FULLreadback.
  ScreenshotINSPECTED OnePluslogo Androidforensic only, notXNU/iOSsuccess.
- Actualprior5202 nativeP-8 at20.0516883s: stream1 vendor done01980000=26738688,
  total024ace08=38456840. Approx1.2717MiB/s; vendoraloneestimate28.84s, thus
  20s necessarilytoo short. Fullknownthreehashstreams+secondrescuepass need
  measured-throughput-based larger boundedbudget; NOThang/unknownstream now.
- PRIVATEboundedagent fixesreturnreadabsence accounting+strictcompleted-return
  ancestorvalidation (originalfailedcontroller remainsfailed); notsharedyet.
  NativeknownP-8Fastbootreasonproposal611db6c5...6dc9 host68/ARM64PASS defaultoff,
  trueEL1MMIO/EL3retention/LKpriorityunproved. CEalignedstateproposalalsoPRIVATE.
- AllphonehandlesTERMINAL; ecdb firmwareFastboot ready; no manualactionpending.
  No userdata/GPT/protected/slotwrite. GoalACTIVE, no actualiOSusability.

## ACTIVE HANDOFF: pairedecdb installed; automatic forensic readout LIVE (2026-10-21)

- Writer24783 TERMINALrc0 one64MiBboot_b ACK Sending1.385s/Writing0.138s/
  total1.525s. INSTALLEDecdb9763fdf5ed6edf658cb5bb61f964ffacf760d96669f14186850250c3f5e5,
  token60f7a088784bf748/prior5202a9b5b44f0392. ACKONLY/lastFULL784e. RETAIN.
- Wrapper/controller48892 LIVE USBobserverreadybeforeboot, private
  ace-ram-sha-block-forensic-20261021/phone-trial. PollSAME48892 neverrestart.
  Needcurrenttoken/rootB/fullboot/vendor/priorprogress/AEE/screeninspection/
  strictADBreturn/physicalFastboot. NoXNU/no seed/norescue; no successclaim.
- Previouseff7 trialmanualrecovery; latestmanualrequest fulfilled. No userdata/
  GPT/protected/slotwrite. GoalACTIVE, actualiOSnotyetusable.

## ACTIVE HANDOFF: scalar manualFastboot verified; pairedecdb ready (2026-10-21)

- Controller36664 TERMINALrc1/300s noADB; independent64714 TERMINALrc0 all19
  observations180s noFastboot/ADB. Finaladbdevices+mdns headers only. Manualhelp
  requestedonlyafterlostsoftwarechannel; USERnowconfirmsmanualFastboot.
  Freshidentity-boundreadback product/B/unlocked/firmwareallrc0; appendednew
  truthfulmanualobservation andmanual-recovery-verified.json, no oldfactsrewritten.
- Conditionalpackage84637 TERMINALrc0 actualfailure+manualFastboot/sourcepins/
  5QEMU/fullring/exactpackage/backups/eff7ACK+784eFULLancestry PASS. Newforensic
  ecdb9763fdf5ed6edf658cb5bb61f964ffacf760d96669f14186850250c3f5e5,
  token60f7a088784bf748/prior5202a9b5b44f0392, noXNU/no seed/noRAMrescue,
  originalgeneric/pinnedAndroid. Standinghumanapprovedforensicexception.
- Nextoneguardedwrite/readout, noecdbwriteyet. Actualscalarprogress/causeUNKNOWN.
  Keep experimentalimage, no userdata/GPT/protected/slotwrite. GoalACTIVE.

## ACTIVE HANDOFF: scalar eff7 failed300s; extended readonly observer LIVE (2026-10-21)

- Controller36664 TERMINALrc1 after300s noADB, consumedwriter33604rc0/ACKONLY
  eff7f170d8c684d5968b16c480bdf9d6bf128a5880f73a449d48c8b8bfed3c66,
  lastFULL784e. No currenttoken/pstore/progress/RAMstage/screenshot recovered;
  cannotinferwhethernewhash passed orremainsbudgetlimited. Retain eff7.
- IndependentREADONLYobserver64714 LIVE up to180s, first08:47:40UTC noexpected
  Fastboot/ADB. PollSAME64714; no restart consumedcontroller. No manualrequest
  yet, no currentsoftwarechannel. Private extended-readonly-usb.json captures.
- Pairedforensic37420 TERMINALrc0 native+5QEMU/fullringpreservation PASS,
  ace-ram-sha-block-forensic-20261021 onlyprebuilt. NOpackage/candidate/ledger/
  write untilactualpostfailure firmwareFastboot. Ifreturns, package exactfresh
  token60f7a088784bf748/prior5202a9b5b44f0392 once thenreadactualcause.
- NativeknownfailureFastbootreason minimalproposal andCE alignedstateproof
  remainPRIVATE agentwork; no actualvalidation/deployment/no sharededitslive.
- No userdata/GPT/protected/slotwrite. GoalACTIVE, iOSnotyetusable.

## ACTIVE HANDOFF: scalarblock eff7 installed; automatic physical trial LIVE (2026-10-21)

- Writer33604 TERMINALrc0 exactlyone64MiBboot_b ACK Sending1.386s/
  Writing0.133s/total1.520s. INSTALLED
  eff7f170d8c684d5968b16c480bdf9d6bf128a5880f73a449d48c8b8bfed3c66,
  token5202a9b5b44f0392, ACKONLYpendingreadback/lastFULL784e. RETAIN.
- Wrapper/controller36664 LIVE USBobserverreadybeforeboot, private
  ace-ram-sha-block-20261021/phone-trial. PollSAME36664 NEVERrestartconsumed
  writer/controller. NeedactualRAM/no_data/token/rootB/fullboot/vendor/logs/
  screenshot/strictreturnFastboot. Nextfailuretracecontainsstream/done/total.
- Sharedruntimefrozen. Pairedforensic37420 offlineprebuild; conditionactual
  failedprimary+postfailureFastboot beforepackaging. No manualactionpending.
  No userdata/GPT/protected/slotwrite. GoalACTIVE, no iOSsuccessclaim.

## ACTIVE HANDOFF: scalarblock eff7 ready; guarded write NEXT (2026-10-21)

- Locald1f820b integratesSHA/progress. Build98562 TERMINALrc0 same0118/profile3/
  production20s+150s; candidateeff7f170d8c684d5968b16c480bdf9d6bf128a5880f73a449d48c8b8bfed3c66,
  token5202a9b5b44f0392, fresh3entry+Centry andexact6guard95972PASS with140B
  progress/s0/unchangedrecord+SP/once. ParentactualCtrace95636PASS.
- Offlineprepare44530 latestFULL784e ancestry/backups/newtokenabsence/allsource/
  artifact/contracts gates; freshone-timewriter+controller. Nextonewrite/controller.
  Paired60f7a088784bf748 agentprebuild/sourcefreezeonly, packagingconditionalon
  actualprimaryterminalfailure+postfailurephysicalFastboot. Neverfakefuturefailure.
- Phone784e FULLverifiedFastboot beforewrite. No userdata/protected/GPT/slotwrite.
  Keep currentcandidateaftertrial. GoalACTIVE, iOSnotyetusable.

## ACTIVE HANDOFF: scalar SHA block/progress integrated; fresh candidate building (2026-10-21)

- Integrated4fileprivatepatch b7af8bda230eee2bea6d806ee3dbcc431a5cc71b264988557323d4462cdff77f:
  full64B SHA directinput, onlytailsbuffered; samefullSHA/pins/two-passchecks/
  production20s budget150s guard/STOP. New optionaldisjointcallerprogress tracks
  stream/completed/total, oldbudget APIcompatible, initrd/result unchangedonrefusal.
  OncecurrentownedACERAMERR now140B adds s/done/total; no perchunkpmsg writes.
- Private ace-ram-sha-progress-20261021 reports:112old+112new hashlibvectors,
  65539B/755randomsegments,105actualARM/QEMU MMU/C/IoffPASS. icount ratio.848
  onlyinstructionmodel, NOTphysicalspeed. ActualC trace/STOP/crossresetprefix/
  nearfull/stalePASS; parent8initrdtestsPASS. Manifest addsdirect64/progressv1.
- Freshbuild98562 LIVE ace-ram-sha-block-20261021 token5202a9b5b44f0392,
  explicitpriorFULL784e. Nextexact3+C/6guardprogresschecks/preparation/guarded
  oncewrite/controller. No newphonewriteyet. Phone784e retainedFastboot.
- PrivateCE prototypepassed112actualEL1QEMU/hashlib+CPACRrestore; no deployment:
  physicalFPtrap/isars/CPACRunknown, inputunalignedstaging/wholeSIMDrestore proof
  needed. NO MMU/cachechange. Nextphysicaluses scalar only.
- No userdata/GPT/protected/slotwrite; no manualactionpending; goalACTIVE.

## ACTIVE HANDOFF: forensic784e fullreadback; production20s also timedout (2026-10-21)

- Controller43641 TERMINALrc0 ADB28.1s/current64c6739a80da715a/rootB/
  fullboot784e7e3a41d5d6fb09a831d93deadeabe337fd75d29e3b04a0b78f3876711872
  +vendor verified, completeAEE/pstore/dmesg, one strictrefreshedADBreturn and
  physicalfirmwareFastboot verified. RETAIN784e FULLreadback; allphonehandles
  TERMINAL. diagnostic_only_return_verified=true; normalautomatic_loop false.
  ScreenshotINSPECTED entirelyblack Androidforensic, noXNU/iOSdisplayclaim.
- Actualpriorbd72 pmsg P rc=-008 ticks0f98df13=20.128986076923077s,
  choseninitrd66f00000..69c1292c. Fullpmsg19876B SHA
  beda002a99aa05486f21aa285b2e30f0846b64dd5d7a21ff8110adbe6b8522d9,
  saved ace-ram-budget20-forensic-20261021/pmsg-budget20.bin. Still native
  preparebudget failure BEFORE RAMLinux; doNOTassumeprogressstream/offset.
- ParallelPRIVATE fixes: bounded_root_failure exactscalar SHA direct64B blocks
  (old perbytebuffer addsuncachedwrites) +boundedprogressdiagnostics; ram_recovery
  independent performance/optionalSHA2hardwareinvestigation. No shared editsyet.
  Need cryptographic equivalent/actualARM tests before newtrial, no blindbudget
  expansion. ExactAndroid dmesg uses sha256-ce, but nativeEL1FPpermission unproved.
- Private ace-guard-park-proposal-20261021 ARMhelper13472B SHA9c4492793bfecb757530d27f87707ac9361423ad4ac31724a34cc3649117f3c2,
  actualhost pidfd/proc/oneSIGSTOP+T/refusaltests PASS, noSIGCONT. Still actualRAM/
  namespace/uniqueguard/pmsg/longHWwatchdog/window/writerreceipt integration needed.
- No userdata/GPT/protected/slotwrites. LatestprimaryFastboot wasUSERmanual;
  latestforensic return softwareverified. GoalACTIVE; actualiOSnotyetusable.

## ACTIVE HANDOFF: paired784e installed; diagnostic readout LIVE (2026-10-21)

- Writer47640 TERMINALrc0 one64MiBboot_b ACK Sending1.383s/Writing0.142s/
  total1.527s. INSTALLED784e7e3a41d5d6fb09a831d93deadeabe337fd75d29e3b04a0b78f3876711872,
  token64c6739a80da715a/priorbd72e6c3eff3ec49. ACKONLY/lastFULL99d8, retain.
- Wrapper/controller43641 LIVE USBobserverreadybeforeboot, private
  ace-ram-budget20-forensic-20261021/phone-trial. PollSAME43641 neverrestart.
  Need currenttoken/rootB/fullboot/vendor/priorACERAMERR/AEE/screeninspection/
  strictADBreturn/physicalFastboot. NOXNU/no seed/norescue. No successclaim.
- Previousb4e8 failed300s; USER manualFastboot, notautomaticreturn. No pending
  manualrequest. No userdata/GPT/protected/slotwrite. GoalACTIVE.

## ACTIVE HANDOFF: budget20 failed300s; user manual Fastboot; forensic784e ready (2026-10-21)

- Controller66696 TERMINALrc1 noADB300s. b4e8 remainsACKONLY/lastFULL99d8.
  Independentreadonly08:27:18UTC actualfirmwareFastboot/product/B/unlocked all
  rc0. USERthenreports manually restoringFastboot: attribute return to manual
  help, exacttimingunknown, NEVERautomaticreturn success. Private separate
  manual-recovery-user-report.json; frozen primaryevidence not rewritten.
- Conditionalpairedpackage97422 TERMINALrc0 onlyafteractualfailure+Fastboot;
  sourcefreeze/exact5QEMU/ringunchanged/fullpackage/extraction/backups/ACK+
  full99d8 ancestry/finalprimarymanifest PASS. Candidate
  784e7e3a41d5d6fb09a831d93deadeabe337fd75d29e3b04a0b78f3876711872,
  token64c6739a80da715a/priorbd72e6c3eff3ec49. NoXNU/no seed/noRAMrescue,
  originalgeneric/pinnedAndroid, samepreviouslyapprovedforensicexception.
  Nextoneguardedwrite+independentreadout; no784ewriteyetatcheckpoint.
- NeedactualACERAMERR/AEE to establish nextfailure, no guessing20s outcome.
  No userdata/GPT/protected/slotwrite. GoalACTIVE, actualiOSunusable.

## ACTIVE HANDOFF: budget20 b4e8 installed; physical automatic trial LIVE (2026-10-21)

- Local013b45e commits measured timeout fix. Writer65613 TERMINALrc0 one64MiB
  boot_b ACK Sending1.386s/Writing0.153s/total1.541s. INSTALLED
  b4e8bb788d579f4105e34e7aebc3060c647891471f5c6b575ead670182aaf51a,
  tokenbd72e6c3eff3ec49; ACKONLYpendingfullreadback, lastFULL99d8. RETAIN.
- Wrapper/controller66696 LIVE, USBobserverreadybeforeboot, private
  ace-ram-budget20-20261021/phone-trial. Poll SAME66696, NEVER restart consumed
  writer/controller. Up to300s: need actualRAM/no_data/rootB/currenttoken/full
  boot/vendor/logs/screenshots/strictreturnFastboot. No successclaim.
- Shared53candidate sourcepins frozen whilelive. Pairedforensic15081 prebuild
  only, realfailure+postfailurephysicalFastboot gates must precedepackaging.
  No userdata/GPT/protected/slotwrite, no manualaction requested. GoalACTIVE.

## ACTIVE HANDOFF: physical RAM validation timeout established; budget20 candidate built (2026-10-21)

- Prior forensic53923 TERMINALrc0: ADB28.1s/current14073d33f8016fef/rootB/
  FULLboot99d87d3f8f435373e7156a2dc22a78dccd706a944a0e339379b95d30c0297a50
  +vendor/strictoneADBreturn/physicalfirmwareFastboot verified. RETAINED99d8.
  Screenshot inspected black Android forensic only; no XNU/iOS claim.
- Actualprior0a9167c0e1bb6647 ACERAMERR1 P rc=-8 ticks199ea1f=2.066473769s,
  initrd66f00000..69c1292c; independent exactELF AEE stage9/-8 and identical
  pmsg crossproof. Native preparation exceeded2s; RAMLinux NOT entered.
- Minimal production validation budget20s/260000000ticks, same two-pass hash/
  layout/latch gates and150s RAM guard. Native manifest records exact budget.
  Build4504 TERMINALrc0: ace-ram-budget20-20261021 tokenbd72e6c3eff3ec49,
  candidateb4e8bb788d579f4105e34e7aebc3060c647891471f5c6b575ead670182aaf51a,
  fresh3entry+CentryPASS/sameaccepted0118; no kernelCI needed.
- Exactcandidate6guardQEMU45125 TERMINALrc0 all6PASS; offlineprepare99568
  TERMINALrc0 latest99d8fullancestry/backups/tokenabsence/hashcontractsPASS.
  Freshone-timewriter/controller ready; nextoneguardedwrite/onecontroller. Pairedforensic agent prebuild only; package gated by actual
  terminalfailure+laterphysicalFastboot. NOnewwrite yet at checkpoint.
- No userdata/GPT/protected/slot changes. Independent no_data RAM recovery and
  long-write guard parking remain prerequisites. GoalACTIVE, iOS not usable.

## ACTIVE HANDOFF: pairedforensic99d8 installed; readout LIVE (2026-10-21)

- Writer66015 TERMINALrc0 one64MiBboot_b ACK Sending1.361s/Writing0.143s/
  total1.506s. INSTALLED99d87d3f8f435373e7156a2dc22a78dccd706a944a0e339379b95d30c0297a50,
  token14073d33f8016fef/prior0a9167c0e1bb6647, ACKONLYpendingreadback.
  LastFULLb906, intervening9f8bACKONLYfailed300s. Retain99d8.
- Independentwrapper/controller53923 LIVE USBobserverreadybeforeboot;
  private ace-ram-guard-code-forensic-20261021/phone-trial. PollSAME53923,
  neverrestartconsumedwriter/controller. Needcurrenttoken/rootB/fullboot/vendor/
  priorACERAMERR/AEEcurrentstage9/screeninspection/strictADBreturn/physical
  firmwareFastboot. NoXNU/no seed/norescue, explicitpreviouslyhumanapproved
  forensicmethod. DoNOTcallreadoutnormalautomaticXNUsuccess. No userdatawrites.
- LKreasonreportcomplete/closedREA: ace-lk-fastboot-reason-20261021/findings.md,
  actualFDTwatchdog1c007000/reboot-modeoffset24maskfvalue3 matchesLKsetter/getter
  cachedreadandclear; rawassemblyneeded(resetpseudocodeoverpruned). Noactual
  EL1MMIO/resetretentionproof/noimplementation. Nochange mainlineworkflow yet.


## ACTIVE HANDOFF: guard9509 failed300s; physical Fastboot seen; paired99d8 ready (2026-10-21)

- Controller9509 TERMINALrc1 after300s noADB; 63836 consumedACKONLY9f8b,
  lastFULLb906. Observer script independentREADONLY finished immediately at
  firstobservation07:58:10UTC (~403s after07:51:27start): expectedfirmwareFastboot,
  product/B/unlocked/is-userspaceno allrc0. Actualreturntime/causeUNOBSERVED;
  nohostreboot/manualrequest. Primaryevidencefrozen bypairedmanifest now.
- Pairedprebuilt43319 native+5QEMU/full64KiBpreservation/3AndroidreadbackPASS.
  Conditionalpackage71411 TERMINALrc0 ONLYafteractualfailedprimary+actual
  postfailureFastboot gates, sourcefreeze44/currenthashes/backups/fullpackage
  extraction/ACK+lastFULL ancestry pinsPASS. No falsefuturefailure fabricated.
- Fresh independentforensic candidate99d87d3f8f435373e7156a2dc22a78dccd706a944a0e339379b95d30c0297a50,
  token14073d33f8016fef/prior0a9167c0e1bb6647. Sameaccepted0118/pinnedAndroid/
  originalgeneric, noXNU/NOseed/NOrescue. PreviouslyHUMANapproved forensicmethod
  standingexception retainedtruthfully. Nextoneguardedwriter thenreadoutonce;
  no99d8writeyet atcheckpoint. ExpectactualACERAMERR orstage9code beforefix.
- LKREAfoundstaticvolatilebootreasoncandidate; nottested/NOdeviceMMIOwrites,
  notmainlinechange. GoalACTIVE, no userdata/GPT/protected/slotwrite.


## ACTIVE HANDOFF: guard-code9f8b installed; automatic physical trial LIVE (2026-10-21)

- Locald80423d integrated6filediagnostics. Writer63836 TERMINALrc0 exactlyone
  64MiBboot_b ACK Sending1.386s/Writing0.137s/total1.525s. INSTALLED
  9f8b0d7927900ffc30df73310e3baf88b7438688869d4277c2a732afe113371e,
  token0a9167c0e1bb6647, ACKONLYpendingreadback; lastFULLb906.
- Wrapper/controller9509 LIVE, USBobserverreadybeforeboot, private
  ace-ram-guard-code-20261021/phone-trial. PollSAME9509; neverrestartconsumed
  writer/controller. <=300s ADB. Needactualcurrenttoken/pstore trace guardrc/
  rootB/fullboot/vendor andstrictFastbootreturn; no successclaim.
- Ifterminalfailure, separateboundedREADONLYlateUSBobservation (last465s),
  verifyphysicalFastboot4fields, thenandONLYthen conditionalpairedforensic
  ace-ram-guard-code-forensic-20261021 package-reviewed.py/write/controller;
  itsnative/QEMU prebuild43319 TERMINALrc0 alreadydone, noforensiccandidateor
  ledger/writes. Parentreviewed pair_gates.py: actualfailure+lateFastbootrequired,
  success/live/unknown forbids forensic. Sourcefreeze44files, donotmodifyruntime
  whilethiscandidate/controllerlive. No userdata/GPT/protected/slot changes.


## ACTIVE HANDOFF: guard-code diagnostic9f8b ready; paired forensic prebuilt (2026-10-21)

- Integrated6fileminimalRAMdiagnostics: validcurrenttoken/latch-owned pmsg
  once107BASCII P/C rc+ticks+validatedinitrdstart/end; noeviction/seed/reboot/
  controlrecordchange. FIRST/RESCUEonly, STOP/unknown/nearfull unchanged.
  RAM-onlystage9fallbackword20/10groups; existingexceptionstage8 andnonRAM
  9groups/.text.bootbytes+relocs unchanged. Agent11actualARM/QEMUcasesPASS,
  actualintegratedC STOP/currentrecord/ring/unknown casesPASSparentrerun.
- Freshprimary50808 TERMINALrc0: ace-ram-guard-code-20261021 candidate
  9f8b0d7927900ffc30df73310e3baf88b7438688869d4277c2a732afe113371e,
  token0a9167c0e1bb6647, sameaccepted0118/profile3/production2s+150s unchanged.
  Fresh3entry+Centry andEXACTcandidate6guardQEMUcases24071PASS: actualprepare
  fixture-102 ->stage9/102/sameSP+record/oncecontext. Notphonecauseclaim.
- Offlineprepare78366 TERMINALrc0: actualcurrentb906 forensicancestry(fullhash/
  rootB/vendor/strictreturn/Fastboot), backups/freshtokenabsence/currentallsource/
  artifact+QEMUdumps pinned. Initialprivateprepare missingforensic manifestkey
  correctedBEFOREwriter/statecreation (no deviceIO). Freshwriter/wrapper ready;
  nextonewrite/controller. No9f8bwriteyet atthischeckpoint.
- Pair plan research/ace-ram-guard-code-plan-20261021.json; forensic14073d33f8016fef
  /prior0a9167c0e1bb6647 prebuilt43319 TERMINALrc0, 5QEMU PASS/fullringunchanged.
  Sourcefreeze44files ace-ram-guard-code-source-freeze-20261021.json. NOforensic
  candidate/ledger/write yet: packagingONLYifactualprimaryterminalfailure and
  lateractualFastboot4identityfields; primarysuccessforbidsforensicwrite.
- Phoneb906 FULLverifiedretainedfirmwareFastboot/allphonehandlesTERMINAL;
  no manualaction/nouserdata/GPT/protected/slotwrite. GoalACTIVE.


## ACTIVE HANDOFF: exact AEE cannot recover guard rc; next diagnostic fix private (2026-10-21)

- FinalactualAEEanalysis ace-ram-rescue-forensic-20261021/aee-analysis/findings.md:
  CPU0PC4000176c/LR40000108/SP44610040 exactnativependingstage5/-67halt;
  word20fallbackerror notencoded. AEE reportsMRDUMPpercpusignaturefailure/
  coredumpfetchfailure, 55CRCvalidentries have no native record/GPR/native
  stack. DFDopaque notdecoded, no claimofexhaustivebitproof. ActualrcUNKNOWN.
- bounded_root_failure implementingPRIVATEminimaldiagnostics: currentvalidowned
  pmsg onceASCII P/C errortrace(noeviction/seed/reboot/controlrecordchange),
  RAM-onlywatchdogstage9=actualnegativeword20 with10groups; oldstage8exception
  bucket preserved/nonRAM9groups unchanged. NeedactualARM+QEMU beforemerge.
  NoXNUCIneeded/no actualcauseguess. Agentmayincludeelapsed/initrdcontext ifsmall.
- Builderupdated explicit --verified-prior-trial andselected --entry-case,
  preservesdefaultall+Centry. Actualcurrentb906 approvedforensic/fullreadback/
  token/strictreturn/Fastboot ancestryPASS; 11agentofflinecasesPASS. Parentalso
  tightened<=3readobservations/complete-differentstop andexactmissing-device
  conditionforsecondreturnattempt. Currentactualb906 passes0.228s/30pins.
- Phoneb906 FULLverifiedretainedfirmwareFastboot; no livephoneprocess/manual
  action. No userdatawrite. Nextfresh3entry+C/newdiagnosticcase, guardedwrite/
  controller once, inspectactualcode beforechangingguard. GoalACTIVE.


## ACTIVE HANDOFF: forensicb906 full readback; native RAM prehandoff failure established (2026-10-21)

- Controller61559 TERMINALrc0 ADB28.1s/fullbootb906fc87137c2499fb392f8505195e29f54c3e2843822508a39c2285c64a4e44
  +vendor/rootB verified, allAEE/logscomplete, strictrefreshedrecord/oneADBreturn/
  physicalfirmwareFastboot verified. INSTALLEDb906 FULLREADBACKverified RETAINED.
  diagnostic_only_return_verified=true, normalautomatic_loop_verified=false
  intentional; noXNU/no pmsgseed inforensic. ScreenshotINSPECTED entirelyblack
  Androidforensic only, noXNU/iOSdisplayclaim. AllphonehandlesTERMINAL.
- Retainedpmsg19836B SHA f0f96650fbc7248225cc4b2cbe52a2dd60bd3f8934c21517fb16ab2696685474:
  EXACTLYONE priorcurrenttoken3785...entry+armed+BSDfirstmountfailure; ZERO
  ACEANDROIDhandoff/ACERESCUEselected/ACE_RAMDIAG. Thusactual0f2aXNUroot path
  proven, RAMLinuxhandoffNOTobserved; failurebeforehandoff.
- AgentactualAEE decryption+CRC: uniqueprior-token db.fatal.02.HWT.dbg SHA
  14d791687e6b3ed81d2ad3a901e090efb4df939aa2f20ba38d80084da46d782d.
  TFA CPU0PC4000176c/LR40000108/SP44610040: exact0f2aELF stage5/-67halt-slot
  branch, LRafterrefusalreturn. Confirmsnativepending-returnguardhalt, NOTRAM
  Linuxfailure. Actualword20rcstillUNKNOWN; agentcheckingGPR/stack evidence.
- Nextfixmustbeestablishedfailure/diagnosticblindspot, neverassumehashbudget.
  bounded_root_failure privateonceappendcurrentvalidringtrace+optionalRAM-only
  haltx3=word20proposal, actualARM/test beforeintegration; noreset/ABI/PCchange.
- Nouserdata/protected/GPT/slotwrite. Rootwriterexclusionfixedprivately9tests,
  but independentno_data/guardpark longstream preconditionsunmet. GoalACTIVE.


## ACTIVE HANDOFF: forensicb906 installed; independent readout LIVE (2026-10-21)

- Writer64015 TERMINALrc0 one64MiBboot_b ACK Sending1.385s/Writing0.160s/
  total1.547s. INSTALLEDb906fc87137c2499fb392f8505195e29f54c3e2843822508a39c2285c64a4e44,
  token810e83565e8cb277/prior3785c625abbd0b07, ACKONLYpendingreadback.
  LastFULL15da; intervening0f2aACKONLYfailed300s+latefirmware465s.
- Independentwrapper/controller61559 LIVE, observerreadybeforeboot; private
  ace-ram-rescue-forensic-20261021/phone-trial. PollSAME61559, neverrestart
  consumedwriter/controller. Explicitforensicexceptionpreviouslyhumanapproved,
  noXNU/no seed/no RAMrescue. Needcurrenttoken/rootB/fullboot/vendor/priorring/
  AEE/screenshotinspection, strictoneADBreturn/physicalfirmwareFastboot.
  DoNOTcallthisnormalXNUautomaticloop success. Retainb906; no userdatawrites.


## ACTIVE HANDOFF: late Fastboot verified; fresh forensicb906 ready (2026-10-21)

- Extendedreadonlyobserver92754 TERMINALrc0: expectedfirmwareFastboot observed
  07:12:39UTC (~465s aftertrialstart07:04:54), productk6895v1_64/B/unlockedyes/
  is-userspaceno allrc0. No hostreboot/userkeys, latecauseUNOBSERVED. No manual
  requestsent. Prior0f2a remainsACKONLY/lastFULL15da. Oldtrial evidence frozen
  now bynewforensicmanifest; doNOTmodifyitsstate/observer files.
- New independent ace-ram-rescue-forensic-20261021 candidateb906fc87137c2499fb392f8505195e29f54c3e2843822508a39c2285c64a4e44,
  fresh810e83565e8cb277/prior3785c625abbd0b07, sameaccepted0118/pinnedAndroid/
  originalgeneric54961d...90d2. Explicitdiagnostic-only NOXNU/NOseed/NOrescue,
  samepreviouslyHUMANapproved forensicexception persisted, no newapprovalclaim.
- FiveQEMU full64KiBbefore/afterunchanged, threeactualAndroidguestreadbacks;
  full64MiB/native/source/backup/failedACK+lastFULL+actualdelayedFastboot ancestry
  pinsPASS. Parentcheck-offline PASS0.921s. Newwriter/controllerUNCONSUMED;
  nextoneguardedwrite thenindependentforensicreadout. No b906writeyet.
- Diagnosticblindspot confirmedsourceonly: RAMprepare/commit rc existsword20,
  EL3haltPCencodesoriginalstage5/-67 only; x0/x1/x2 overwritten. Agentpreparing
  privateappend-only token-boundfailure trace aftervalidownedpmsggates, wait
  actualforensicresult beforeintegration. No actualcauseinferred.
- Rootwriterexclusivegapfixedprivately9tests/ARMpass; guardpark/no-data gates
  remainunverified. GoalACTIVE, no userdata/GPT/protected/slotwrite.


## ACTIVE HANDOFF: RAM/rescue300s no ADB; software USB channel absent (2026-10-21)

- Controller64696 TERMINALrc1 at07:09:55UTC after300s noADB, phase
  no-adb-after-300s-no-retry. Writer78728 consumedTERMINALrc0. INSTALLED0f2a
  ACKONLY(no fullreadback), lastFULLverified15da. No nativecurrentrecord/pstore/
  RAMstage/Androidrescue/screenshot recovered; cannotattributefailuretoRAM or
  hashbudget yet. ActualUSB observeronlyinitialremove+root-hubchange55s, no
  deviceadd; finalobserverterminated. No userdatawrite/restore/blindreboot.
- Independentreadonly07:09:53 noexpectedFastboot; actual lsusb no phone; adb
  devices andmDNS containheaders/no services. Extendedreadonlyobserver92754 LIVE
  up to120s (separatefromconsumedcontroller), outputs extended-readonly-usb.json.
  Pollsameobserver; neverrestart failedcontroller. No manualrequestyet atthis
  checkpoint. Actualfailurelostsoftwarechannel; manualmaybenecessarylastresort.
- ram_recovery preparingindependentHUMANpreviouslyauthorizedforensic method:
  freshdiagnostic-only/prior3785c625abbd0b07/noXNU/no pmsgseed/noramrescue,
  sameaccepted0118/currenttools/originalgeneric. Private
  ace-ram-rescue-forensic-20261021, no writes. NeedactualFastboot first.
- TouchREAcontract ace-touch-protocol-20261021/contract.md +15records: bounded
  identify02/app20/descriptor25 readpaths, wireA5/code/lenLE16/payload/5A,
  continuationA5/03. OEMread_message canqueueRUN_APPLICATION14, soindependent
  allowlisteddispatcher needed, notwholeOEMcallbackreuse. Staticonly/current
  descriptorstillunknown, sessionsclosed.
- Rootwriterprivate reviewfoundglobalwriterexclusion gap, beingfixed; also
  exactguardparkreceipt/pidfdneededbeforelongwrites. StillNOTallowedexecute.
  GoalACTIVE; originaluserdata/backups/protected/GPTintact.


## ACTIVE HANDOFF: RAM/rescue0f2a installed; automatic physical trial LIVE (2026-10-21)

- Local193f497 integrated19fileboundedRAMrescue. Writer78728 TERMINALrc0,
  exactlyone64MiBboot_b ACK Sending1.384s/Writing0.151s/total1.538s.
  INSTALLED0f2a4058c2088a38133f094934e950968c85f97526f0627bb209407d55eec054,
  token3785c625abbd0b07, ACKONLYpendingfullreadback; lastFULLverified15da.
- Wrapper/controller64696 LIVE withUSBobserverreadybeforeboot; pollSAME64696,
  NEVERrestart consumedwriter/controller. Private ace-ram-rescue-physical-20261021/
  phone-trial, deadline300s. NeedactualRAMstage ordependentAndroidrescue label,
  currenttoken/root/B/fullboot/vendor/logs/inspectscreen/strictoneFastbootreturn.
  No successclaim/no manualactionpending. Retain0f2a; no userdata/otherwrites.
- Offline rootwriterproposal ready6hosttests/staticARMELF, no deviceIO/no repeated
  16GiBhash. NOTreadyexecute: requiresverifiedindependentRAM andparkedterminal
  session. Agent analyzing150sguard park/safePIDidentity beforelongUSB2write;
  rootwrite remainsblockedbytheseconcretepreconditions, goalACTIVE.


## ACTIVE HANDOFF: bounded RAM/rescue candidate0f2a ready; guarded write NEXT (2026-10-21)

- Integrated frozen19fileRAM/rescue proposal (privatepatch a34765ec...afe35),
  preserves approved-reseed builder/verifier; onlyrelocationfixture404->401 to
  keep largerImagewithin45000000. FiveRAMcontroller/actualdeadline testsPASS
  2.006s; eightinitrdtestsPASS0.276s; diffcheckPASS. Reviewer found noblocking
  deadline/extent/one-retry issues afterstaleverifieroverwritefixed.
- tools/ace-build-ram-rescue.py freshproduction build16347 TERMINALrc0:
  private ace-ram-rescue-physical-20261021 candidate0f2a4058c2088a38133f094934e950968c85f97526f0627bb209407d55eec054,
  token3785c625abbd0b07. Sameaccepted0118kernel4f425/profile3, freshlyrebuilt48
  modulesRAMgeneric8804457B, derivedrescuecapsule preservesoriginalMagiskblob.
  Productionhashbudget2s/guard150s; noQEMUrelaxationinphoneimage. Freshall9native
  +actualCentryPASS withFINALverifier, full64MiB/extraction/source/contractpins
  PASS. No claimthatunenabledseed2wasexecuted inthese9cases.
- Parentprepare6050 TERMINALrc0 addsreportverifier/dumphashes+fullcurrent15da
  normalauto/fullboot/vendor/rootB/strictreturn/physicalFastboot ancestry,
  freshtokenabsence, originalbackups; freshone-timewriter/controllerwrapper.
  NEXT writerONCE thenwrapperONCE; observe<=300s. Pending->firstRAM, exactfatal
  or150sverifieddeadline->oneAndroidcapsule, consumedSTOP. Earlynativefaults
  outsidecoverage; hardware2sthroughput/reset/USBstillunproven. No writeyet.
- Currentphone15da FULLverifiedretainedFastboot. No userdata/GPT/protected/slot
  changes. Rootwriterproposalofflineonly, no16GiBrepeatedhash/no deviceIO.
  GoalACTIVE, actualiOSrootmount/display/touch notverified.


## ACTIVE HANDOFF: 0119 exact CI kernel accepted; RAM deadline coverage being finalized (2026-10-21)

- CI39556379040/job119076997707 SUCCESS on2d756a8910d2651ed48f122b0a1478f30546d7db,
  cached130s/1071hits2misses, artifact12325118502 ZIPf333339b217d86f036650a94cf5fec8dec514aad52f83d52c74c51270e816dff.
  Exactacceptedkernel17592360B SHA5105d9d302723bbe35441bdabaf0f1f1b9ec093ab12adc839783dc3881490d59,
  private ace-gated-aks-proposal-20261021. All84oldcriticalstrings, exactlinked
  registryuniqueAKSpersonality/currentACEhardware, gatecalls/exact4Bcompare,
  symbols/cachemaintenance/provenance/SHA256SUMS PASS. Notphysicallybooted;
  currentprofile3stilldisablesAKSstart. Actualcachedmetrics notestimated.
- RAMagent QEMU7fullproofready; firstpreinitfatal covered, but downstream
  module/USBfailure originallynotactive-resetcovered. Parentauthorizednecessary
  one150sdeadlineguardonlyafterexactRAMcapability/currentrecord/oldringrestore;
  timeout rechecksidentity thenonewarmreset, unknownstateparks. Privatetargeted
  test/QEMUshortdeadline thenfreezecompleteproposal+realbuildscripts. Avoid
  addingunrelatedscope. Controllerbudgetmustcover150s+Android. Realreset/timing
  stillneedsphoneproof; no-data recoveryNOTyetverified/userdatawriteNOTyetallowed.
- ios_root_readiness nowofflinepreparingboundedrawrootwriterproposalonly,
  no new16GiBhash/no devicecommands, executionrequiresfutureverifiedno_data
  recovery. Phone15da retainedFULLverifiedFastboot; no manualactionpending.


## ACTIVE HANDOFF: 0119 cached CI39556379040 LIVE; RAM full reset proof ready (2026-10-21)

- Local6ca730c new0119 gates softwareAppleKeyStore service on exactrd=aceufsroot0
  anddefaults/no-effaceable-storageexact4BLE1; selectorsunchanged/noSEP. Six
  actualACE/SWEETcompilesPASS/SWEETcode-data-relocsunchanged/allimportslinked.
  Public5testsPASS0.134s afterfixingtest toskipunrelatedbinarypatchbeforeUTF8
  decode (testfixpendingcommit). Actualorder82..119fuzz0applyPASS againstCI81
  baseline; initial1..81patchesbyteidentical. No liveAKSregistrationclaim.
- Remote2d756a8910d2651ed48f122b0a1478f30546d7db exactonepatch parent8d6cca,
  blob76bb0f695b71edb2915d0b9c215d68e6fa648654 verified. OnecachedACE/diagfalse
  run39556379040/job119076997707 LIVE; private ace-gated-aks-proposal-20261021/
  ci-state.json. Browseractualrun/screenshot saved+embedded. Nextacceptexact
  artifact/provenance/hash/metrics; doNOTdispatchagain. No0119devicewrite.
- RAM qemu-reset7 PASS actualsingleprocess Linuxfatalwarmreset -> nativeone
  rescue -> secondLinuxwrapperEL0 -> originalMagiskinitEL0PC207d10 ->hostreset
  ->STOP-106/nothirdjump. Physicalpmemsave shows wrapperpreservesselectedprefix
  afterLinuxclearsring; nextresetpmsgunchanged. Production2shashbudgetNOTyet
  hardwareverified (QEMU-only20s). Agent refreshingcompleteproposal/builder
  merge with330a1dd andrealphonepackage+controllerpins; old12filediffINCOMPLETE.
- REAtouchreport ace-touch-minimal-20261021/findings.md: actualS3910modules/FDT
  SPI2/IRQ/GPIO/dependencies; resetcanupdatefirmware underDTenabledflag. DoNOT
  callOEMreset/probeasreadonly. NextpassiveAndroidinput/IRQcapabilities; actual
  S3910firmware/descriptorstillunknown. AllREA sessionsclosed.
- Phone15da FULLverifiedretainedfirmwareFastboot, allphonehandlesTERMINAL,
  automaticloop78.2s verified; rootwrite stillwaits independentdatafree recovery.


## ACTIVE HANDOFF: fresh-token full BSD read + one root failure + auto return VERIFIED (2026-10-21)

- Wrapper/controller65449 TERMINALrc0, diagnosticADB78.2s, currenta8df6ac99033e368,
  root/B/fullboot15da26400dda43c51eb8bc23a15e04ee2252fa23c3687a6eb88ec88177c051b0
  +vendor verified. Full logs/AEE complete, strict refreshedrecord/oneADBreturn/
  actualfirmwareFastboot verified; automatic_loop_verified=true. INSTALLED15da
  FULLREADBACKverified, RETAINED. No manualactionneeded; allphonehandlesTERMINAL.
- Actualfirstnative record stage7/error0/seed1: thisboot zone was ALLZERO and
  legacyseed1 ran. Exact archivedseed2 remains QEMUonly; doNOTclaimphysicalseed2.
- Retainedpmsg20104B SHA3b26ccce416aadb05fe628d0dd32c0be4a9143f890de26e3d54caf8851e99dfe
  has EXACTLYONE currenttokenentry+armed, fullGPTcrc b989cbd8, userdataLUN2
  first3514368 blocks58961912, actualop7 GOOD+first4096CRC b74108f5, readonly
  BSD aceufsroot0 major1/minor0 ready. EXACTLYONE HFSsignaturecf70/rooterrno19/
  firstfailureparking. This freshly binds0116/0117/0118 hardware path and proves
  preservedlatch/autoreturn afterfirstrootfailure. No HFS/iOSmount success.
- Screenshot SAVED/INSPECTED Androidhome+USBdialogonly. Currentuserdata still
  Android unchanged, HFSfailureexpected. Derivednojournal16GiBiOSroot ready,
  but independent no-data recovery still REQUIRED beforeuserdataoverwrite.
- Nextmainline RAMrecovery actualsecondLinux wrapper->Magiskentry nowobserved,
  finalSTOPproof/privatecontroller manifest andphysicalRAMtiming/evidence next.
  Agentbounded_root_failure reviewingprivateproposal; profile4+gatedAKS private
  proposal actual6ARMcompiles/5gatetests PASS, notmerged/noCIyet. GoalACTIVE.


## ACTIVE HANDOFF: reseed candidate15da installed; automatic trial LIVE (2026-10-21)

- Local330a1dd integrated exact-snapshot reseed/tests. Writer7019 TERMINALrc0,
  exactlyone64MiBboot_b ACK Sending1.383s/Writing0.141s/total1.527s.
  INSTALLED15da26400dda43c51eb8bc23a15e04ee2252fa23c3687a6eb88ec88177c051b0,
  tokena8df6ac99033e368, ACKONLYpendingfullreadback; lastFULLverified6ea.
- Wrapper/controller65449 LIVE withUSBobserverbeforeboot, private
  ace-pmsg-approved-reseed-20261021/phone-trial. Poll SAME65449; neverrestart
  consumed writer/controller. Needcurrenttoken/rootB/fullboot/vendor/logs/
  inspectscreen/strictreturnrecord+ADBreturn+physicalFastboot. No successclaim.
- RAMagent QEMU6 actuallyreached wrapperEL0 and originalMagiskinit entry207d10;
  GDBvirtualreadharnessfailed, nowusingphysicaldump forfinalSTOPproof. Private
  proposalstillnotphysicalready. Retain15da; no userdata/protected/GPT/slotwrite.


## ACTIVE HANDOFF: exact archived reseed candidate ready; guarded trial NEXT (2026-10-21)

- Integrated explicit 64KiB exact archived-snapshot reseed API/CLI; only full
  match permits seed2, valid/zero legacy0/1 unchanged, unknown zone untouched.
  Capture remains private. Five synthetic host tests PASS0.247s; actual ARM
  native link + fresh5 QEMU entry cases + C entry +2 Android readback PASS.
  Near-match case differs ONLY final byte and verifies full unchanged snapshot;
  initial assertion expected old1 nonzero, corrected to actual sum5 and rerun
  all5 fresh. Initial outputs retained; no phone retry involved.
- New private ace-pmsg-approved-reseed-20261021 candidate15da26400dda43c51eb8bc23a15e04ee2252fa23c3687a6eb88ec88177c051b0,
  tokena8df6ac99033e368, accepted unchanged0118kernel4f425b...054c6/CI39551656841.
  Full package/hash/embedded archivedcapture0c9011...36c50/Android/backups/
  freshsource/report/dumps gates PASS. Prepared fresh one-time writer/ledger
  from actual CURRENT6ea fullreadback+stage5/-64snapshot+guardedADBreturn/
  physicalFastboot, explicitly NOT prior normalautomaticloop success.
- NEXT run guardedwriterONCE then run-auto-once.pyONCE with observer ready;
  inspect actual currenttoken XNUentry/root firstfailure/preserved latch and
  automatic return. No new candidate write yet at this checkpoint. Phone6ea
  retained firmwareFastboot, no manual action requested. No userdata/protected/
  GPT/slot changes. Parallel RAM rescue proposal still NOT physical ready;
  actual secondLinux wrapper/Magisk entry under QEMU investigation. GoalACTIVE.


## ACTIVE HANDOFF: 0118 native seed refusal; first physical full snapshot captured (2026-10-21)

- Wrapper/controller4754 TERMINALrc0: diagnosticADB30.1s, current114d6af2c1976963,
  root/B/fullboot6ea55b77cc23a38505bc4ce4ca4fc3c29ac198aa8c5fdfa9f0baa191d9431ec6
  andvendorverified. Alllogs/AEEcomplete, refreshedreturnrecord/oneADBreturn/
  actualfirmwareFastbootverified. INSTALLED6ea FULLREADBACKverified, RETAINED.
  automatic_loop_verified=false: stage5/-64 BEFOREXNU, notnormalpendingreturn.
- First actualhardwarefailed-seed FULL64KiBsnapshot capture+immutablebracketed
  currentrecord validation PASS. research/ace-bsd-root-failure-20261021/phone-trial/
  pmsg-before-seed.bin SHA0c9011073ff7e45fa5689b7a92f6a05f9385538b9273058a8a61a70e9db36c50.
  Header0/0/0, exactly4nonzero bytepositions 0x4462=11,e46c=80,e47a=08,e47e=10;
  no pstoremember/currentXNUentry. NoRAMrepair/clearoccurred. Therefore0118
  firstfailureparking stillNOTphysicallyexecuted/verified. Screenshot INSPECTED
  AndroidhomeUSBdialog, notXNU/iOS. Originaluserdatastillintact.
- Next minimalblockerfix delegated privately to ios_root_readiness: explicit
  hash-pinned captured-zone reseed ONLYafterordinaryownedRAM/ECC0/type0 existing
  gates, onlyentire64KiBbyteidentitywithalreadyhost-retainedcapture. Good/zero
  defaultpathsunchanged, unknowncontentrefuses/snapshots unchanged. No arbitrary
  ignore4bytes/headrepair/wholesaleunknownRAMclear. Proposal/test/ARMproofbefore
  integration; currenthumanexplicitsoftwaremodification+mainlineauthorization.
- RAMrescueagent realQEMU found Linux movesnativepmsg tooldpstore/clearslive;
  proposedPID1 republishesONLYvalidatedcurrentoldring oncebeforefatalwarmreset.
  ActualLinuxpreinitfatal->restart->nextnative nowselectsrescue, TCGproduction2s
  hashbudget exceededsoQEMU-onlyrelaxedbuildexplicitlylabeled; production2skeep.
  AfterrescueLinuxselectedlatchcanalsobecleared: agent preparing wrapper/contract
  plusactualmulti-reset QEMU. StillnotdatafreeUSBsuccess/notphonepackage.
- REAdisplayreport ready ace-lk-display-20261021/findings.md: static32bpp/align32
  dimensions/3buffers+64KiBround matchVRAM candidatepitch4352, realFDTfbfe1af000
  size1e50000 regmatch; NOcurrentstride/format/scanoutproof; cacheclean+explicit
  trigger required byLK code. Interior16KiB read-onlymap canavoidunownedpadding;
  fullfbmappingextrahead0x3000/tail0x1000notowned. AllREA sessionsclosed.
- iOSprofile4 privateproposal andnojournal16GiBroot ready. AKSreview: code
  alreadylinkedACE, onlypersonalitymissing; pureSWunlockedshimcouldbeprofile4
  gated, create/save/load/wrap/unwrapunsupported (notSEP). No firstmountdependency.
- Allphone/build/writerhandlesTERMINAL, no manualactionpending. ThreeAgents
  parallelprivate; parent solephonecontrol. GoalACTIVE, noiOSmount/GUIclaim.

## ACTIVE HANDOFF: 0118 installed; normal automatic trial LIVE (2026-10-21)

- Writer42414 TERMINALrc0 exactlyone64MiB boot_b ACK Sending1.383s/Writing0.135s/
  total1.520s. INSTALLED NOW6ea55b77cc23a38505bc4ce4ca4fc3c29ac198aa8c5fdfa9f0baa191d9431ec6,
  token114d6af2c1976963; ACKONLYpendingfullreadback, lastFULLVERIFIEDforensic74de.
- Wrapper/controller4754 LIVE private ace-bsd-root-failure-20261021/phone-trial,
  USBobserverreadybefore normalreboot. Poll SAME4754; neverrestart consumed
  writer/controller. ExpectoneHFSrooterror/oneparking andretainedentry/latch;
  require actualcurrenttoken/root/B/fullboot/vendor/logs/screenshotinspection,
  strictrefreshedrecord/oneADBreturn/physicalfirmwareFastboot. Notyetsuccess.
- No otherpartition/GPT/userdata/protected/slotwrite, retainexperiment; allfresh
  CI/source/criticalQEMU/image/backup/ancestrygates passed asbelow. Parallelagents
  remainprivate(no sharedsourcechanges). GoalACTIVE; noiOSmount/display/touch.

## ACTIVE HANDOFF: 0118 focused checks PASS; candidate ready; guarded write NEXT (2026-10-21)

- CI39551656841/job119062006502 SUCCESS cached179s/1072hits1miss exact8d6cca8c803041b95c0ce2db80e0e29a6621478a.
  Artifact12324550175 ZIP5ca48e6dcb613a1f0d7d16c361b085026379148e5cca429aa1a2f4db1a56713c,
  acceptedkernel17575976B SHA4f425b1716c6802b07fea6d373bac366126515f66735d69e55ce10038f5054c6.
  Exactprovenance/SHA256SUMS/entry/newfirstfailuremessage/BSDsymbols/cachesync PASS.
- Build79704 TERMINALrc0 focused3entry(actual/phoneaddress/auto-reset-refusal),
  actualCentry + pendingAndroiddurablecurrentrecord PASS. Unchangednative source
  hashes identicalto historical0117baseline, full9+6reports retainedasreuse
  references; notclaimedfreshallcases. Package/prepare87678 TERMINALrc0,
  full64MiB candidate6ea55b77cc23a38505bc4ce4ca4fc3c29ac198aa8c5fdfa9f0baa191d9431ec6,
  freshtoken114d6af2c1976963. Allsources/reports/backup/fullpackageextraction/
  embeddedAndroid/currentforensic74de fullreadback/returnancestry pins PASS.
- Freshnewtoken absentpriorforensicevidence; exactoneboot_bwriterreviewed,
  no reboot/restore/otherwrites. Next writerONCE/controllerONCE; expectoneHFS
  invalidsignature thenonefirstfailureparking, preservedentry/token andnormal
  autoreadout (mustphysicallyverify; no inferredsuccess). NO0118writeatcheckpoint.
- ParallelREA completed andsessionclosed: private ace-lk-ram-layout-20261021/
  findings.md has Evidence IDs/rawbytebinding. Initrd66f00000, vendor->generic
  ->config/footer; footerphysicalalignmentnotguaranteed; mb_ramdisk freedbefore
  finalFDT, alloc-rangesfuturecandidate notwholeallocateddomain. RAMagent using
  this proof forprivateguard/codecupdate andactualmulti-resetQEMU/controller.
- PrivateiOSprofileproposal complete6tests/5ARMcompiles, 0..3ADT/manifest/payload
  unchanged, newcanonical4=3016B; notmergedwhilecurrentcandidate sourcefixed.
  HFSsourceaudit confirms512logical/4096physicalworksat241GB; no earlyioctlpatch.
  Rootnojournal derivative readyasrecordedbelow. No userdata/protectedwrites.

## ACTIVE HANDOFF: 0118 CI39551656841 LIVE; parallel RAM/REA/root profile (2026-10-21)

- OnecachedACE/diagnosticfalse workflow41 on exact8d6cca8c803041b95c0ce2db80e0e29a6621478a,
  job119062006502. Local4279069 includes0118 + optionalcaseverifiers (default
  allunchanged). Private ace-bsd-root-failure-20261021 pipeline now3freshentry
  cases(actual/phoneaddress/auto-reset-refusal)+Centry+1pendingAndroidreadback,
  historical9+6reports onlyreused if every native sourcehash matches exactly.
  Physicalidentity/backups/recovery/currenttoken/fullhash andCIexact gateskeep.
- User explicitly invokedREA and statesauthorization fordeep software/hardware
  analysis/modification. Parentread /home/xu/.agents/skills/reverse-engineer-anything/SKILL.md.
  bounded_root_failure nowownsREA native session, targeted originalAceLK initrd/
  alloc-ranges vsreg analysis using existingreviewedwrapper/snapshot. RAMagent
  preparing privateintegrationdiff; current12ARMcompiles/FDT6tests/PID1badtoken68/
  actualprepare-commit mockRAM transitionsPASS, syntheticlayoutlink79695872B only;
  realLKlayout/actualmulti-resetQEMU/controllerrescuecontractstillneeded.
- Rootagent READY derivative research/ace-ios-root-readiness-20261021/ios16-root-readonly-nojournal.img,
  17179869184B SHA cfa5610d2f6afa4cb03dde8b186e5cb0452e774e5d7462465a8ad5ded590dcf4.
  fsck-f-n rc0/nonjournaledcase-sensitiveHFS appearsOK. Completeoriginal/derived
  comparison onlyoffset1030/17179868166 0x21->0x01, primary/backupattrsjournaled
  bitclear; allApplefilebytes/JIB/journalunchanged. Copy47s/12.15GBallocated,
  oncefullSHA+compare55.516s; originalimg/simgintact. DoNOTflasholdjournaledsimg.
- Rootagent nowpreparing explicituserspaceprofile privatepatch: 3knownargs
  ignition_level=1/unentitled_ios_sim_launch=1/launchd_unsecure_cache=1 plus
  defaults/no-effaceable-storage neededpastkeybag. Existingprofile3 unchanged.
  Ace maxdownload64MiB; nosparseuserdatawritephysicalproof, don'treuseSweet-S512M
  ordd .simg. IndependentdatafreeADB recovery mustbeverified beforeboundedraw
  userdatarootwrite. No userdata/GPT/protected/slotchanges; goalACTIVE.
- Phone currentlyfullverifiedforensic74de retainedfirmwareFastboot; allphone
  controller/writerhandlesTERMINAL, no0118writeyet. NextacceptCI/criticalchecks,
  freshnormalauto candidatefromtruthfulforensicreturnancestry, oneguardedwrite/
  controller. Parent solephonecontrol; parallelagents privateonly.

## ACTIVE HANDOFF: forensic recovered root-loop evidence; 0118 ready; parallel work (2026-10-21)

- Forensic92184 TERMINALrc0, ADB28.1s/current5fcd36892b2170f4, root/B/fullboot
  74de374fe978feb3a202c3f1073afb3164489c7c278371b1c0f2f56aae8d4784 andvendor
  verified. Alllogs/AEEcomplete; strictcurrentreturnrecord/oneADBreturn/physical
  firmwareFastboot verified. INSTALLED74de FULLREADBACKverified, RETAINED.
  diagnostic_only_return_verified=true, normalautomatic_loop_verified=false
  intentional; never call forensic readout normalXNUauto success.
- Validfullring65524B SHA7369cbffd3db4ae6b0c53df823848d549a0490756ca47076cb2d0c4bb3c413bb
  contains124 each0117-specific explicitdevice aceufsroot0 major1/minor0,
  HFSinvalidsignaturecf70/rooterrno19. Earliestcurrententry/token/firstop7/CRC
  overwritten: prior_marker_count0, ringvalid0, zone65532nonzero. Thus retained
  unique0117root-stage evidence, attributionfromsoleinstalled0117thenno-XNU
  forensic path; NOTfresh-token-bound fulltrace or verifiedHFS/iOSmount.
  Screenshot SAVED/INSPECTED entirelyblackAndroiddiagnostic only. NoUSERkeysasked.
- Established nextfix: preventfailedmountloop overwritingentry/latch. Agent
  bounded_root_failure delivered0118/test: firstvfs_mountroot error for exact
  ACErd=aceufsroot0 printsONCE/WFEparks, no newwatchdog/SMC programming, successful
  root/nonACE unchanged. ActualbranchhostPASS0.813s,3singlefileACE/SWEETcompiles
  PASS/SWEETcode-data-relocs unchanged/importslinked ABI/WFEdisasmverified.
  Private ace-bsd-root-failure-20261021. Needfreshnormalauto physicalvalidation.
- User explicitly authorized multi-Agent parallelism and skipping unnecessary
  verification forspeed. Delegated rootfailure(nowdone), ram_recovery, and
  ios_root_readiness. Parent ownsallphonewrites/CI. RAMagent preparing private
  rescueintegrationdiff (notsharedsources) forboundedRAM->generic recovery to
  collectrealRAMstage; stilluserdata-dependent, notdatafree success. Rootagent
  found existing16GiB HFSX root research/ipsw-x/ios16-root.img / .simg, static
  arm64launchd/dyld/SpringBoard/entitlements/cache checks, no newdownload/hash
  repetition. Preparinguserspaceargs/writeplan privately; no userdatawrite.
- Parent added optional --case to native/refusal verifiers (defaultallunchanged)
  to avoidrepeatingunchanged6+9cases. Nextkernel stillgets exactCI/hash/entry,
  phoneaddressentry/currenttoken/latch/refusal+Centry+pendingAndroidreadback;
  physicalidentity/backup/fullimage/ancestry gates retained. Source/records
  pinstillmandatory. FulliOSgoalACTIVE; no display/touch/userspace success.

## ACTIVE HANDOFF: forensic74de installed; independent readout LIVE (2026-10-21)

- Writer80069 TERMINALrc0 exactlyone64MiB boot_b ACK Sending1.407s/Writing0.141s/
  total1.549s. INSTALLED NOW74de374fe978feb3a202c3f1073afb3164489c7c278371b1c0f2f56aae8d4784,
  token5fcd36892b2170f4/priorf2a578690ae96c20; ACKONLY pendingreadback,
  lastFULLVERIFIED1422...7997b (interveningcade ACKONLY unverifiedfailure).
- Wrapper/controller92184 LIVE, independentforensic ledger/--diagnostic-readout-only,
  observerreadybeforeboot. Poll SAME92184; neverrestartthisorfailed5316.
  Private ace-bsd-root-forensic-20261021/phone-trial. NoXNUattempt/pmsginit,
  samepreviouslyhumanapproveddiagnosticexception withinboot_bscope.
- NEXT currenttoken/root/B/fullboot/vendor, priorring/token observation,
  pstore/dmesg/AEE andinspectADBscreen, strictrefreshedreturnrecord/oneADB
  reboot/physicalfirmwareFastboot. Separateforensicreturn fromnormalauto
  success. Retainforensicexperiment; nooriginalrestore/userdata/protected/
  GPT/slotwrite. ActualpreviousBSDcauseunknownpendinglogs; goalACTIVE.

## ACTIVE HANDOFF: fresh forensic package verified; single diagnostic write NEXT (2026-10-21)

- Independent ace-bsd-root-forensic-20261021 candidate74de374fe978feb3a202c3f1073afb3164489c7c278371b1c0f2f56aae8d4784,
  fresh5fcd36892b2170f4/priorf2a578690ae96c20. Sameacceptedkernel566ad2...1826d,
  --diagnostic-readout, NOXNUattempt/NOinitializepmsg/NOauto-XNU, pinnedAndroid
  originalgenericdiagnosticramdisk (notoriginalbootrestore). FiveQEMUcases PASS,
  threeguestreadbacks/onesyntheticpriormarker, everypstorebefore==after.
- Package33318 TERMINALrc0 full64MiB/source/artifact/embeddedAndroid/backup/
  fullpackageextraction/priorfailedtrial/newtokenabsence pinsPASS. Concrete
  forensicrequest validatorPASS. Freshwriteroneboot_bonly/noreboot reviewed.
- Authorization uses alreadyHUMAN-approved diagnostic-only method noted earlier
  (forensic-consolefix0 explicitexception reply), persistedacrossturns plus
  currenthumanmainline/automationcontinuation. No newapproval inferredfromtick;
  no expansiontoGPT/userdata/protected/slots. Explicitforensicexceptiongate kept.
- Currentphone lateverifiedfirmwareFastboot; installedcade ACKONLY, previous
  fullverified1422. NEXT writerONCE thenindependent run-forensic-once.pyONCE
  (controller --diagnostic-readout-only), observerbeforeboot. Do NOTrestart
  failed5316 orclaimnormalautomaticloop fromforensicreturn. Capture/readreal
  previouslogs ifRAMsurvived; screenshotsAndroidonly. GoalACTIVE.

## ACTIVE HANDOFF: 0117 no ADB; late firmware Fastboot recovered; forensic NEXT (2026-10-21)

- Controller5316 TERMINALrc1 after150s noADB, phase no-adb-after-150s-no-retry;
  observer stopped. No pstore/currentrecord/fullboot/vendor/screenshot from
  this trial. Installedcade2b...9e88f ACKONLY, lastFULLVERIFIED1422...7997b.
  No actualXNU/BSD/root/device-success claim. Do notrestart consumedcontroller.
- ExtendedREADONLY observation0 at181s: noADB/Fastboot and no phoneUSB inlsusb.
  Observation1 at264.3s: EXPECTEDserialFastboot returned. Refreshedphysical
  productk6895v1_64/B/unlockedyes/is-userspaceno allrc0. Late return cause
  UNOBSERVED (observeralreadyterminal; nohostrebootaftertimeout). No manual
  request sent/useractionobserved. Evidence retained in failedtrial directory.
- NEXT independent forensic recovery following previously approved diagnostic
  exception method: fresh --diagnostic-readout/--prior-run-token f2a578690ae96c20,
  noXNUattempt/noinitializepmsg, samecurrentacceptedkernel/pinnedAndroid/original
  genericramdisk, nooriginalrestore. Freshsource/artifact/hash/backup/identity
  checks and controller/ledger; NEVERrestart consumed5316 or blindlyreboot.
  Prepare concrete forensic package + QEMU preservation proofs before write.
- Prior forensic method explicitly approved by human after workflowexception
  request (NOTES forensic-consolefix0); latestuser continues/requestsautomation.
  Any forensic controller must retain diagnostic_only_exception_authorized gate
  with truthful authorization basis; no protected/GPT/userdata/slot writes.
- FulliOSgoalACTIVE, actual0117failurecauseunknownpendingrecoveryevidence.

## ACTIVE HANDOFF: 0117 installed; automatic physical trial LIVE (2026-10-21)

- Writer74801 TERMINALrc0 exactlyoneboot_b64MiB ACK Sending1.386s/Writing0.156s/
  total1.544s. INSTALLED NOWcade2bbbf1104669baf09a69ab2d295e71b25107c2ec223598fa13620179e88f,
  tokenf2a578690ae96c20, ACKONLY pendingfullreadback; lastFULLVERIFIED1422...7997b.
- Wrapper/controller5316 LIVE private ace-bsd-root-entry-20261021/phone-trial;
  USBobserverready before normalreboot. PollSAME5316, neverrerun consumedwriter/
  wrapper/controller. ExpectedADB150s; collectcurrenttoken/root/B/fullboot/vendor/
  screenshot/pstore/dmesg/AEE, inspectactualearlyroot/op7/BSDCRC/device/errors.
  Require refreshedcurrentrecord/identity and oneguardedADBreturn to actual
  firmwareFastboot. Retaincade experiment, no routine restore/manualkeys.
- No otherpartition/GPT/userdata/protected/slotchanges; allsource/CI/preflight/
  backup/hash/newtokenabsence gates passed. FulliOSgoal ACTIVE/unachieved.

## ACTIVE HANDOFF: 0117 fresh exact candidate ready; guarded write NEXT (2026-10-21)

- Build40628 TERMINALrc0 all9native+Centry+6Android PASS, exactkernel566ad2...1826d
  CI39548458101/job119051920073 cached214s/1072hits1miss. Package/prepare36397
  TERMINALrc0 full64MiB bootcandidatecade2bbbf1104669baf09a69ab2d295e71b25107c2ec223598fa13620179e88f,
  fresh tokenf2a578690ae96c20, explicitroot/normalauto/pmsg/failedseedcapture.
  Fullpackageextraction/generic/pinnedAndroid/backup/source/reporthash gates
  passed; tokenabsent from actual prior1422trial evidence. Priorinstalled1422
  verifiedfullreadback/root/B/vendor and automaticFastboot ancestry pinned.
- Freshone-timewrite-bsd-root-once.py reviewed exactoneboot_bflash/noreboot,
  nootherwrites. Statefreshauthorized; no0117writeyet at checkpoint. NEXT
  guardedwriterONCE thenrun-auto-once.pyONCE withobserverbeforeboot, inspect
  actualearlyroot/op7/BSDproof/errors and currenttoken/fullhash/autoreturn.
  Currentphone1422 retainedFastboot, no manualactionpending; goalACTIVE.

## ACTIVE HANDOFF: 0117 exact kernel accepted; native preflight LIVE (2026-10-21)

- CI39548458101/job119051920073 SUCCESS exactb1205f3d9d574c0e88cf85aab558d1e4ace02f0c,
  cached214s/1072hits1miss. Artifact12322292938 ZIP99142238687f85395a368aa24726122a424b21ae800ae092b7d510b783774553,
  acceptedkernel17575976B SHA566ad266fdcb8da9954b9a2b0bd00b4b19a3967d95fd6b3af95325cf5001826d.
  Exactprovenance/SHA256SUMS/entry+earlyrootstrings/BSDsymbols/cachesync PASS;
  realCIlog/accepted-provenance/screenshot privateace-bsd-root-entry-20261021.
- Build40628 LIVE native9+Centry+6Android verification. NO0117phonewrite, nofresh
  writer/controllerconsumed. RetainedphoneFULLVERIFIED1422...7997b in firmware
  Fastboot. NEXT finishpreflight/package/prepare fresh token+ancestry, thenone
  guardedboot_bwrite/controller withobserverbeforeboot. Inspectactualearlyroot/
  op7/BSDread/device/errors; maintaincurrenttoken/identity/fullreadback/autoreturn.

## ACTIVE HANDOFF: 0117 cached CI39548458101 LIVE (2026-10-21)

- One dispatch workflow40 on exactb1205f3d9d574c0e88cf85aab558d1e4ace02f0c,
  job119051920073 inprogress, ACE/cached/diagnostic_artifacts=false. Local
  2e89d92+handoff33f30a1. Private ace-bsd-root-entry-20261021 ci-state and
  exactaccept/build/package scripts pinnedcurrentrun/job/commit. No rerundispatch.
- NEXT pollthisrun, acceptsuccess exactartifact+metrics, native9+Centry+6Android,
  package/freshtoken/current1422fullverifiedancestry, guardedonewrite/oneauto.
  Phone remainsfullverified1422...7997b in firmwareFastboot, RETAINED; no0117
  write or livephonecontroller. Prior56127/78852 consumedTERMINAL.
- Physical0116 onlyproviderready, noBSDread; genericIOBSDwait hypothesis from
  source, earlyselectorlogs are the nextrealverification. FulliOSgoalACTIVE.

## ACTIVE HANDOFF: 0117 early explicit BSD root selector ready; CI dispatch NEXT (2026-10-21)

- Local2e89d92 / remoteb1205f3d9d574c0e88cf85aab558d1e4ace02f0c:
  new0117 moves exact rd=aceufsroot0 selection before generic30s IOBSD wait,
  with entry/result logs and same bounded sleeping provider/BSD read gates.
  Default/nonACE behavior unchanged; original assertionline numbers restored.
  12actualACE/SWEETcompiles/imports PASS/SWEETcode-data-relocs unchanged;
  actualselectorbehavior testPASS0.558s (wrong/defaultnames untouched, exact
  root/error propagation). No claim about physicalwaitcause beyond hypothesis.
- NEXT cachedACE/diagnosticfalse CI fromb120, exactaccept/preflight/package,
  fresh token with lastFULLVERIFIED1422...7997b ancestry, oneguardedboot_bwrite
  and oneautomatictrial; inspectactualearlyroot/op7/BSDproof/mountresult.
  Private work research/ace-bsd-root-entry-20261021. Existing1422 phone retained
  in verifiedfirmwareFastboot; no0117write/currentcontroller/liveprocess.
- All previouswriter/controller consumedTERMINAL; useractionnone. GoalACTIVE.

## ACTIVE HANDOFF: 0116 provider READY; no BSD read reached; Fastboot verified (2026-10-21)

- Wrapper/controller78852 TERMINALrc0: ADB76.2s/currentfb46d809f2fb6bae,
  root/B/fullboot1422a2ddf623a75789665fd16ad4e75054b4c4d42e536e6191d567f49687997b
  andvendorbb5a09...9670 verified. ALLdiagnosticscomplete; firstAEEtar partial
  retained, secondidentity-refreshedtar complete. Onecurrentrecordmatch/one
  ADBreboot/physicalexpected firmwareFastboot B/unlocked/is-userspaceno verified.
  Observerstopped. INSTALLED1422...7997b nowFULLREADBACKverified, RETAINED.
- Actual currenttokenXNUentryEXACTLYonce; GPT/header/allfourarrayreads succeed,
  CRCb989cbd8/userdata3514368+58961912 confirmedagain. NEW providerphase1
  readiness published. NOop7/BSDreadproof/devfs/rootmount log; lastBSDstage
  calling setconf. Thus real BSD IO stillUNPROVEN; don'tclaim BSDmount/iOS.
- Source shows IOFindBSDRoot waits up to30s for genericIOBSDresource BEFORE
  the explicitACErootbranch. This is a SOURCE-BACKED SUSPECT, not yetphysical
  waitentry/exit proof. NEXT0117 ACE exactrd=aceufsroot0 earlyrootpath before
  generic matching/allocations, bounded sleepingproviderwait and entry/result
  logs. BuiltinHFSalreadyregistered in actualvfsinit logs. Keep default/nonACE
  pathunchanged, physicalBSDreadproof required. No speculativemediawrites.
- Screenshot saved/INSPECTED Androidhome+USBdialog only. pmsg19065B SHA
  50a030f65d0815145d38e22d8aaeafaf4e874a74a5283d5c13b2f9c08af060f9.
  Private trial-conclusion.json records observations vs hypothesis. No manual
  action/recoverypending. NoGPT/userdata/protected/slot/restore writes.
- All localwriter/controller/buildhandles TERMINAL. Do notrerun consumed.
  FullgoalACTIVE; rootfilesystem/userspace/display/touch stillunverified.

## ACTIVE HANDOFF: 0116 BSD root image installed; automatic trial LIVE (2026-10-21)

- Writer56127 TERMINALrc0: exactlyone64MiB boot_b write ACK, Sending1.385s/
  Writing0.148s/total1.536s. INSTALLED NOW1422a2ddf623a75789665fd16ad4e75054b4c4d42e536e6191d567f49687997b,
  tokenfb46d809f2fb6bae; ACKONLY pendingfullreadback, lastFULLVERIFIED1089...ae294.
- Wrapper/controller78852 LIVE, USBobserverready before normal reboot, private
  ace-ufs-bsd-root-20261021/phone-trial. PollSAME78852, neverrestart consumed
  writer/wrapper/controller. ExpectedADB150s; collectcurrenttoken/root/B/fullboot/
  vendor/screencap/pstore/dmesg/AEE, inspectactual op7/BSD CRC/device/root errors.
  Strict refreshedcurrentrecord and guardedoneADBreturn to firmwareFastboot.
- No otherpartition/GPT/userdata/slot/protected/restore, no manualactionpending.
  FulliOSgoal ACTIVE/unachieved. Keep experimental1422 retained. Build/source/
  provenance and allpreflights/backup/tokenabsence gates passed as below.

## ACTIVE HANDOFF: 0116 exact root candidate ready; guarded write NEXT (2026-10-21)

- Build95264 TERMINALrc0, all9native+Centry+6Android preflights PASS on exact
  acceptedkernel e5a381...5dbb8/CI39546747819/job119046526281. Package/prepare
  15321 TERMINALrc0, full64MiB candidate
  1422a2ddf623a75789665fd16ad4e75054b4c4d42e536e6191d567f49687997b,
  tokenfb46d809f2fb6bae, explicit rd=aceufsroot0 and readonly root capability.
  Exactsource/reports/dumps/fullpackage-extraction/generic/Android and original
  boot+vendor recovery hashes PASS. New token absent from all prior trial
  evidence; actual current1089...ae294 fullreadback ancestry pinned.
- Fresh state authorized/awaitingfinalbootloaderchecks; writer write-bsd-root-once.py
  reviewed: exactlyone boot_b flash, no reboot/restore/otherwrites. Freshcontroller
  notlaunched. NO0116phonewrite at this checkpoint; retained1089 firmwareFastboot.
- NEXT invoke guardedwriterONCE (identity/product/B/unlocked/firmware/size gates),
  then run-auto-once.pyONCE with USBobserverbeforeboot. Poll those exacthandles,
  collectactual op7/BSD CRC/device/rootmount result and inspect screenshot,
  verify refreshedcurrentrecord and oneADBreturn to firmwareFastboot. No repeats.

## ACTIVE HANDOFF: 0116 exact kernel accepted; native preflight LIVE (2026-10-21)

- CachedCI39546747819/job119046526281 SUCCESS remote4d664ae5627c909ad523c7b666a92ee577d13a55.
  Real build194s,1070hits/3misses; source/KDK/compiler caches restored. Accepted
  artifact12322500880 ZIPf3cc27069861056e3089d05a8b14fc06ddc7712bf7b881ed1ebeb25f4e5dbf45,
  kernel17575976B SHAe5a381caf8316b4a413ba36b06771e434399811ad227c2532c87cee44675dbb8.
  Exact run/SHA/provenance/SHA256SUMS/entry + new BSD symbols/strings and real
  cache-maintenance disassembly PASS. Logs and accepted-provenance private.
- Build95264 LIVE: fresh native77594624B SHA4bf6df6f3939c4279f628ef617816834ea7e8213b3fd26897387a8b3ed4daca7,
  tokenfb46d809f2fb6bae, explicit rd=aceufsroot0/root-device-readonly true,
  pmsg/failedseed-snapshot/init-empty/pinnedAndroid/auto-reset readout retained.
  Await9native+Centry+6Android tests, then package/prepare/write/controller once.
- NO0116phonewrite yet, no fresh writer/controller consumed. Phone retained
  fullverified1089...ae294/tokena7a4e2808d9016d8 firmwareFastboot. Nouserdata
  or GPT/protected writes. Goal ACTIVE; host/kernel build not physical iOS.

## ACTIVE HANDOFF: 0116 cached ACE CI39546747819 LIVE (2026-10-21)

- Remote4d664ae5627c909ad523c7b666a92ee577d13a55/current workflow39
  job119046526281 in progress, cached/diagnostic_artifacts=false. One dispatch
  only through existing authorized logged-in Edge because gh unauthenticated.
  Source/KDK + compiler caches restored; Build running. UI screenshot private
  ace-ufs-bsd-root-20261021/ci-dispatch.png. Local implementation eab939e.
- Prepared offline accept/build/package/prepare scripts with exact run/job/SHA;
  pending accepted new kernel before any native build/package/write. Fresh
  writer/controller NOT consumed or launched; no0116phonewrite. Retained
  physical1089...ae294 and firmwareFastboot remain latest verified state.
- NEXT inspect this exact run, accept artifacts and real metrics, root-enabled
  native/QEMU preflights, hash-pin candidate, prepare fresh token ledger from
  physical1089 ancestry, guarded write once/controller once and inspect logs.
  All host/compile proofs recorded below; actual BSD/iOS still unverified.

## ACTIVE HANDOFF: 0116 readonly BSD bridge implemented; CI dispatch next (2026-10-21)

- Added 0116 ACE-only BSD bdev/devfs + explicit rd=aceufsroot0, reusing retained
  AceUFS singleton/LUN2/GPT userdata bounds. No second HBA init or writes.
  Acquire/release readiness, permanent IOLock serializes all root DMA; narrow
  op7 READ10, strict existing response/host/CRC/guard checks; first fault
  quarantines, no retry. Checked 512-sector/4096-bounce ranges/partial residual;
  all writes rejected. BSD provider wait sleeps <=10s, raw read capped64KiB.
- Actual source12 ACE/SWEET Mach-O compiles PASS; SWEET code/data/relocations
  unchanged (original IOKit assertion line numbers preserved); every import
  linked against prior real kernel plus new bridge symbols. 63UFS hosttests
  PASS14.870s including actual threaded bridge and BSD strategy, 10native
  input testsPASS1.094s. These are host proofs, NOT physical BSD/iOS success.
- Remote exact prior7dc3ba6 -> 4d664ae5627c909ad523c7b666a92ee577d13a55
  on UnrealXu/ios-sweet:codex/ace-initial-platform, only new0116patch published.
  NEXT dispatch cached/diagnostic_artifacts=false ACE kernel from this SHA,
  inspect exact provenance/artifact, root-enabled native/QEMU checks, package
  fresh token/pmsg/pinned Android/auto-readout, guarded one-time boot_b write
  and new automatic controller. Never rerun consumed prior writer/controller.
- Phone remains lastFULLREADBACKverified1089dd...ae294/tokena7a4e2808d9016d8
  in firmwareFastboot, retained; NO0116phonewrite yet. Android userdata still
  intact; no filesystem/iOS/display/touch claim. Independent RAM recovery
  remains required before any iOS userdata replacement. Full goal ACTIVE.
- Private source/compile/test evidence: research/ace-ufs-bsd-root-20261021.

## ACTIVE HANDOFF: PHYSICAL XNU full primary GPT/userdata discovery PASS (2026-10-21 12:41 CST)

- Wrapper/controller28176 TERMINALrc0: diagnosticADB78.1s/currenta7a4e2808d9016d8,
  root/B/fullboot1089dd1777396f84af66c5441d8add4dc8aeee29bad32d2363a20dba6f3ae294
  and vendorbb5a09...9670 verified. ALLlog/AEEcollectioncomplete; one refreshed
  retained288Bcurrentrecordmatch, oneADBrebootrc0, actual expectedfirmware
  Fastbootproduct/B/unlocked/is-userspaceno verified. Observer stopped after
  controller; no manualkeys/user action. automatic_loop_verifiedtrue and
  diagnostics_completetrue. INSTALLED nowFULLREADBACKverified1089...ae294,
  tokena7a4e2808d9016d8, RETAINED. No routine originalrestore/recoverypending.
- Actualcurrenttoken ACEXNU1 entry EXACTLYonce. Genuine UFS primary header0,
  READ10op6 LUN2/LBA2,3,4,5 four4096B DMA completions allOCS0/SCSIstatus0/
  response0/residual0/IS1. FULL16KiBarray CRCb989cbd8 equalsheaderexpected,
  parserresult0; userdata firstLBA0x35a000=3514368, blocks0x383aff8=58961912,
  bytes241507991552. Sourceexplicitly logs discoveryonly/noBSDmedia/filesystem.
  This is real XNU media metadata discovery, not merelatch/Android/QEMU.
- Independent comparison with prioridentity/currenttoken-bound Androidsdc first
  24576B reference SHA43318ec9fadd317eb7face67f8f50bf6134d743947aae53de688b314cc42bdd5:
  Pythonzlib fullarrayCRC and separately parsed exactUTF16 userdata entry79
  bounds matchtheXNUlogs. No fullbyteidentityclaim fromCRC alone. PrimaryGPT
  only, backupGPTnotread. Current pmsg18936B SHA
  0e31b78bb030d95196f88f36714ac555588873bf01bb8d5dafb5824b589b5a8a.
  Private ace-ufs-rsp-header-20261021/phone-trial/trial-conclusion.json.
- Screenshot SAVED/INSPECTED AndroidhomeUSBdialog, NOT iOS/XNUdisplay/touch.
  Currentfullobjective stillunachieved: noBSDdevice/rootmount/iOSuserspace,
  framebuffer/touch/basicoperations. No userdatawrite or GPT/protected/slot/
  backup/restorechanges. OrdinaryAndroidruntimewrites only existingfallback.
- Sourcea37e8de (0115responseheader fix), prior5e907e0snapshotintegration.
  Handoffs76cb5f6/6de09bc/c0e017b. Actualkernel eafb64...dcd183 from successful
  cachedCI39544238227/job119038676572, artifact12320489702 ZIPc1a6bd...866f70,
  171s/1071hits1miss; sixsingle-file ACE/SWEETcompiles/imports/SWEETunchanged,
  60hostUFS testsPASS13.068s,9native+Centry+6AndroidpreflightsPASS. All local
  build/test/download/write/controller handles TERMINAL. Do not rerunconsumed.
- NEXT MAINLINE: implement serialized READONLY BSD root bridge on the retained
  AceUFSowner + validateduserdata bounds. Single IOLock for DMA/commands,
  release/acquire readiness published afterGPT, bounded sleeping wait for
  provider fromBSDroot (notbusyIODelay starving singleCPU). Separate narrow
  root-read opcode limitedtoLUN2/validateduserdata; retainrequestCRC/header/
  residual/OCS/IS/host/DMAguard/quarantineonfirstfailure/no retry. 4096B bounce
  reads with checked512B-sector mapping/EOF/overflow/resid, rejectALLwrites.
  Add ACE-specific bdev/devfs and explicit rd=aceufsroot0 only undernewcapability;
  no secondHBAadoption/reinitialization, noSweetQualcomm/LUN0 transportreuse.
  Existing userdata isAndroid, notHFS: readonlyBSDdevice/readproof mustnotbe
  reportedasfilesystem/iOSmount. Independentno-dataRAMrecovery stillneeded
  before overwritinguserdata withiOSroot. Do not derail workingnormalauto path
  into speculativepmsgrepair; fullsnapshotcapability isready iffailure recurs.
  Keep goalACTIVE; no pendingmanualaction/permissionrequest.

## ACTIVE HANDOFF: 0115 installed; automatic physical trial LIVE (2026-10-21)

- Writer76074 TERMINALrc0, exactlyoneboot_b64MiB ACK accepted Sending1.390s/
  Writing0.144s/total1.535s. INSTALLED NOW1089dd1777396f84af66c5441d8add4dc8aeee29bad32d2363a20dba6f3ae294,
  tokena7a4e2808d9016d8; ACKONLY pendingfullreadback, lastverified63a945...758f6.
- Wrapper/controller28176 LIVE, private ace-ufs-rsp-header-20261021/phone-trial;
  USBobserverready before normalreboot. Poll SAME28176, neverrerun consumed
  writer/wrapper/controller. All9+Centry+6preflights/CI171s/hash/source/backups
  gates passed. ExpectedADB150s; collectactualfullGPT4reads+CRC/userdata bounds
  or nextrealerror; nativefailedseedfullsnapshot ifneeded, noRAMrepair.
- No otherpartition/GPT/userdata/slot/protected/restore, no manualactionpending.
  FulliOSgoal ACTIVE/unachieved. Need inspectrealAndroidscreenshot andlogs;
  neither latchedrecord nor fallbackAndroid alone proves newXNU/root success.

## ACTIVE HANDOFF: 0115 exact candidate ready; guarded write NEXT (2026-10-21)

- CI39544238227/job119038676572 TERMINAL SUCCESS cached171s/1071hits1miss,
  exactremote7dc3ba697cd6f2c94605a3a13b789cb5a052cb14. Artifact12320489702
  ZIPc1a6bd46db4a9d4c3499a2f77a3a73b6295ee658178dc59353cfd3938b866f70;
  acceptedkernel17541904B SHAeafb64d36fd8c0d4c48c780b7566f1130ddfa984eef966dfed5e32fae1dcd183.
  ExactCI/sourceprovenance/SHA256SUMS/entry+UFSstrings/symbols/cachemaintenance
  checks PASS; real restoredsource/KDK/compiler cachemetrics in ci-job.log.
- Build87307 TERMINALrc0 ALL9native+Centry+6Androidrefusal checks. Package/prepare
  69617TERMINALrc0, full64MiB candidate
  1089dd1777396f84af66c5441d8add4dc8aeee29bad32d2363a20dba6f3ae294,
  freshtokena7a4e2808d9016d8. Originalgeneric/Android/boot+vendorbackups intact.
  Exactcurrentreports/dumps/native/kernel/ADT/source/fullpackageextraction pins.
  Previous ACTUALfullreadbackverified63a945...758f6+normalautomaticFastboot
  ancestry and freshmarkerabsence pinned, no old2f/salvage assumption.
- Private ace-ufs-rsp-header-20261021 write-response-once.py reviewed: exactly
  oneboot_bflash/no reboot, finalexpectedserial/firmware/product/B/unlocked/
  geometry/backups/hash gates. NEWstate fresh/authorized/requiredsnapshot true.
  At this checkpoint NO0115phonewrite yet; installed63a945...758f6 retained.
- NEXT invokewriterONCE thenrun-auto-once.pyONCE, observerbeforeboot; verify
  currenttoken/root/B/fullboot/vendor/screenshot/logs/refreshedguardedreturn.
  Hardwaretarget actual4GPTarrayreads/CRC b989cbd8/userdatabounds; NOTBSDroot
  or usableiOS. No userdata/protected/GPT/slot/restore writes or manual action.

## ACTIVE HANDOFF: actual0114 XNU/GPT header proof; GOOD-response false rejection fixed0115 (2026-10-21)

- Snapshot wrapper/controller18445 TERMINALrc0: ADB76.1s, exactcurrentd229token,
  root/B/fullboot63a945c41c90c97e661e176287b74b0497daebfa0c265a255ad6a4f0516758f6
  and vendorbb5a09...9670 readbackverified, all logs/AEEcomplete, screenshot
  SAVED/INSPECTED AndroidlockscreenUSBdialog only. One refreshed288Breturnrecord
  match, oneADBrebootrc0, physicalproduct/B/unlocked/is-userspaceno verified.
  automatic_loop_verifiedtrue/diagnostics_completetrue. Observer stopped with
  controller; no manual action. INSTALLED63a945...758f6 RETAINED, notrestored.
- ExactlyONE actual ACEXNU1:d229...entry marker and embeddednative stage7record
  prove THIScurrentkernel execution; native seed_outcome1 means whole initial
  zone was zero thistrial and legitimatelyinitialized. Prior corrupt-zone cause
  remainsunknown, NOTfixed or reproduced. Snapshot expectedfalse because this
  return is actual pendingtrial5/-67, no failedseed snapshot claimed physically.
- Genuine LUN2capacity4096/last3b95fff, blocks0/1 CRCf59d9d0e/79b497ad and GPT
  header validation0. New READ10op6/LBA2 completed OCS0/SCSIstatus0/residual0/
  IS1, unchangedrequestCRC4140afa0, quietUIC/knownhost. But newlyadded0113 gate
  FALSELY rejects unusedr[32]/r[33]=a5. Actual first32response bytes are
  21000200 +28zeros, next480B leftpoisoned. Current XNU fullarrayCRC/userdata
  bounds still NOTverified. No BSDmedia/rootmount/iOS. trial-conclusion.json
  pinsactualpmsg19034B SHA0d8f23c35b09f58c2620d2bead169a62c7e9f10a35868e7ac4be8a7fe03a7163.
- Source-backed new0115 replacesunusedsense-tail checks with narrow32B GOOD
  responsevalidator: exacttype/LUN2 andallother32Bheader zero incldatasize,
  status/residual/reserved; ignoresunused32..511. Hostcodec + actualpatched
  header6testsPASS0.790s inclactualpoison response, everyheaderbyte corruption,
  variedunusedtails/null/length/LUN refusal. RequestCRC/IS/host/DMAguard/OCS/
  quarantinerequirements unchanged. OfficialLinuxv5.10ufshcd_scsi_cmd_status
  acceptsGOOD without sensecopy; ufshcd_copy_sense_data gatedbydata-segmentlen:
  https://raw.githubusercontent.com/torvalds/linux/v5.10/drivers/scsi/ufs/ufshcd.c
- Local6Mach-Ocompiles40359 TERMINALrc0: ACE/SWEETpass, SWEETcode/data/relocs
  unchanged, everyimport matchesactualkernelABI;60UFS testsPASS13.068s. private ace-ufs-rsp-header-
  20261021 source applies0115after0114; hostheader matchesexactpatch source.
  Localcommita37e8de/remote7dc3ba697cd6f2c94605a3a13b789cb5a052cb14.
  CI39544238227/job119038676572 dispatched ONCE cachedACE/diagnosticfalse, LIVE
  at lastpollBuildstep. Do notredispatch. Privateci-state/build/package/prepare
  scripts in rsp-header dir; NOnewphonecandidatebuilt yet.
  NEXT exactartifact/freshnative/allpreflights,
  preparefrom CURRENT63a945 actualfullreadback/automaticreturn, notprevious2f.
  No need further pmsgrepair investigation while currentpath works. Continue
  established UFSfailure to fullGPT thenserializedBSDrootbridge. Keep fullgoal
  ACTIVE, no userdata/protected/GPT/slot/restore writes andbackupsintact.

## ACTIVE HANDOFF: snapshot candidate installed; automatic controller LIVE (2026-10-21)

- Guarded writer39344 TERMINALrc0, one boot_b64MiB accepted Sending1.385s/
  Writing0.154s/total1.541s. INSTALLED NOW63a945c41c90c97e661e176287b74b0497daebfa0c265a255ad6a4f0516758f6,
  tokend229a912c63d9c1f. ACKNOWLEDGEMENT ONLY pendingactualfullreadback;2f5846
  remains lastverified ancestry. No otherpartition/slot/GPT/userdata/restore.
- Wrapper/controller18445 LIVE. USBobserver ready BEFORE automatic normalboot,
  private ace-pmsg-snapshot-20261021/phone-trial/controller-launch.json. Poll SAME
  18445; never rerun consumedwriter/wrapper/controller. ExpectedADB150s budget.
  Need currentrecord/root/B/fullboot+vendor, snapshotifseed-3 (rawbytes+header/
  count + bracketedcurrentrecord validation), screenshotinspection, logs/AEE,
  refreshed guarded firmwareFastboot return. Do not call refusedentryXNU/iOS.
- Source5e907e0, handoff698d671; latestall9+Centry+6preflightspassed. No manual
  user actionpending. FulliOS/storageBSDroot/display/touch remainsunachieved.

## ACTIVE HANDOFF: full snapshot candidate packaged; one guarded write NEXT (2026-10-21)

- Source5e907e0 complete snapshot native/controller integrated. Refusal29860
  TERMINALrc0 all6cases incl realLinux65536Bproperty readback,4recordreadbacks,
  syntheticpending+snapshotstate clearly flagged. Native capture itself verified
  through9entrycases with exact fullsnapshot/sourcezone preservation. CentryPASS.
- Package21163rc0/prepare-once rc0. Final64MiB candidate
  63a945c41c90c97e661e176287b74b0497daebfa0c265a255ad6a4f0516758f6,
  tokend229a912c63d9c1f, native77594624B SHA159a377f...56ac. Genuine0114kernel
  c68365...93d61d/CI39541641261/job119030497910; originalgeneric54961de2...fa90d2.
  All latestsource/report/dump/fullimageextraction/CI/ADT/Android/backups pinned.
  Newtoken absent actualpretrial evidence. Previous ACTUALfullreadbackverified
  2f5846...6dc4c6 + separate guarded return checked explicitly, not oldercontrol.
- Private ace-pmsg-snapshot-20261021/phone-trial ledger fresh, requiredsnapshot
  capability true. Reviewed writer has exactly one boot_bflash/no reboot, fresh
  finaldevice/product/B/unlocked/is-userspace/geometry/backups/hash gates.
  NEXT write-snapshot-once.py ONCE, then run-auto-once.py ONCE (observer before
  normalreboot), pollsamehandles. NO phonewrite at this checkpoint; installed
  remainsverified2f5846...6dc4c6. Do not restart any consumedwriter/controller.
- Preserve snapshot asopaque privateevidence, no actualRAMrepair in candidate.
  Neither snapshot/Androidfallback nor kernelQEMU equals iOS success. No GPT/
  userdata/protected/slot/restore writes; full goal ACTIVE and unachieved.

## ACTIVE HANDOFF: full failed-seed snapshot integrated, final Android QEMU readback LIVE (2026-10-21)

- Previous turn PROGRESS: exact0114kernel accepted and readonly snapshot FDT
  copier tested. Current change makes snapshot actual native BSS capture after
  seed refusal and existingCPU/FDT/platform/pmsg exclusions. Full65536B copied
  without touching source, readyflag afterdsb; only stage5/-64/seedHEADER-3
  handoff attaches ace,pmsg-before-seed. New native manifest capability true.
- New controller stateflag pmsg_seed_snapshot_required gates collection after
  essential currenttoken/root/B/fullboot/vendor checks. Fresh serial-bound root
  reads bracket snapshot with retained exact before/after record observations;
  any changed diagnosticrecord is fatal/no reboot. Save raw beforevalidation,
  require65536/header3/nonzerocount match native record; hash/privateevidence.
  Missing/malformed snapshot is explicit incomplete logs, never repair/iOSclaim.
  23controller tests PASS0.031s;4FDT tests PASS;59UFS tests PASS14.890s.
- Private ace-pmsg-snapshot-20261021 actual0114kernelc68365...93d61d +2976BADT.
  First build78284 TERMINALrc1 refused ABS64 native_snapshot-minus-physicalzone
  compiler literal BEFORE link/phone. Preserved native-rejected-absolute-pointer.
  Fixed by existing separate freestanding volatile memcpy unit; no relocation
  rule relaxation. Native77594624B SHA159a377fc168fed2edd8b37bac6f40dd461a77edbf068898f1b64590a1b556ac,
  tokend229a912c63d9c1f. All9native preflights PASS incl actual copied65536B
  snapshot equals invalidfixture + sourcezone byteidentical; actualCentry PASS.
- Combined81765 TERMINALrc1 only last newAndroidfixture: QEMU-only largeBSS
  PID1 ELF PT_LOADfilesz0 rejected by pinnedAndroid(error-14). All prior5cases
  passed. Preserved qemu-verified-rejected-pid1-bss-elf. Fixed fixturedata byte.
  Subsequent76241 TERMINALrc1 onlysnapshotread due one sysfsread returning partial;
  sourceFDTproperty bytecheck alreadypassed, Linux record/modules/poweroffpassed.
  Preserved qemu-verified-rejected-single-read. Fixture now <=64reads to exact
  length+EOF; excess/partial/error fails. No actualphone failure claimed.
- CURRENT verifier29860 LIVE, sixAndroidcases including synthetic failedseed
  state for full real Linuxproperty readback. Existing real nativecapture
  tested separately by9caseverifier; do not call syntheticfallbackstatephysical.
  Need full6case result and allfreshsource/verifier hashes before packaging.
- Offline package/prepare/runwrapper scripts prepared, NOT executed. Package
  requires9+Centry+6 with4guestrecord readbacks and1fullsnapshotreadback; exact
  CI39541641261/job119030497910 and kernel/SHA/ADT/Android/backup/report/dump pins.
  Prepare derives from CURRENT actual2f5846...salvaged/separate-return ancestry,
  notolder2b17control, verifiesretainedrecords/fullreadback andnewtokenabsence.
  No current phonewrite/reboot/restore. Installed2f5846... at priorverified
  Fastboot. Next completechecks/commit/package/oneguardedboot_b/autotrialONCE.
  Preserve latestexperiment andbackups; no protected/GPT/userdata/slot writes.
  Full iOS/root/BSD/display/touch goal remainsACTIVE and UNACHIEVED.

## ACTIVE HANDOFF: 0114 exact CI artifact accepted; current native9cases PASS (2026-10-21 12:07 CST)

- Commits1f3176a controller read-evidence/return resilience + seed observation;
  c424b60 optional complete snapshot FDT copier. Both tested/committed. No new
  phonewrite/reboot this turn; all local handles now TERMINAL.
- Nativecheck17556 TERMINALrc0 ALL9preflights including actualhistorical0113
  XNUentry/relocation/phoneaddress/zerozone/pendinglatch and zeroheader/body
  nonzero refusal observation. This includes current FDTcopier source in the
  binary via NULL/0 oldABI, but fullsnapshotnativecapture is NOTintegrated.
  observationcheck44213 alsoterminalrc0 but predates newcopier; use17556 for
  latestsourcebindings. No candidate from these checks is prepared for phone.
- CI39541641261/job119030497910 TERMINAL SUCCESS, exactremote8f275b65...a5d6d,
  cached159s/1071hits1miss; genuine source/KDK/compiler restores in ci-job.log.
  Artifact12320260313 ZIP8dc17bc8b39789e8d99ec750a7d2669df389495cee4ab4471698516637835da7.
  Accepted exact provenance/SHA256SUMS/linkedentry+UFSobservations/symbols/
  cache-maintenance disassembly. Actual0114kernel17541848B SHA
  c6836571936db27dd3ef1444bc51f3a6611abebd3d72c040cc48b163be93d61d.
  Private research/ace-ufs-gpt-misc-20261021/kernel.development.ace and
  linked-kernel.json/accepted-provenance.json. Accept34251/download5172terminalrc0.
  Latest successfulUI screenshot saved/embedded, no duplicate dispatch.
- Fresh physicalread-only UTC04:04:43 expectedproduct/B/unlocked/firmwareFastboot
  verified. INSTALLED remains2f5846...6dc4c6/token6ec5da258b9ff457 (fullroot
  readbackverifiedprevious turn); retained experiment; no manual actionpending.
- NEXT integrate failed-seed full64KiB READONLY snapshot into native refusal
  path + exact current-token Androidproperty read/hash/privateevidence; optional
  copier alone does not collectphysicaldata. Need QEMUnegative/alias/preservation
  and full Androidproperty byte-readback, plus nativeImagewindow/sourcepin/all
  preflights on actualNEW0114kernel before newphonecandidate. Keep normalauto.
  Do not blindclear zeroheader/nonzerobody or relabel oldrefusal as XNU/GPT/iOS.
  After evidence-backed pmsgrepair, actual0114UFS/GPT rootbounds then BSD bridge.
  Independent no-data recovery still required before userdataoverwrite. Goal
  remains ACTIVE/UNACHIEVED; protected/GPT/backups intact, no routine restore.

## ACTIVE HANDOFF: 0114 cached CI live; snapshot-copy foundation tested, not integrated (2026-10-21)

- Source1f3176a committed controller read-evidence/optional log-return handling
  and native zeroheader/nonzerobody observation. Twentyauto tests againPASS
  0.013s/threeAEE0.020s. Earlier observationcheck44213 TERMINALrc0 ALL9 native
  cases, historical0113kernel only. No current-turn phonewrite/reboot/restore.
- 0114 remote8f275b65eb96bf037d2833e4e860727e3afa5d6d; cachedACE13.5DEVELOPMENT,
  diagnosticfalse dispatched ONCE. CI39541641261/job119030497910 confirmed LIVE
  Build step via GitHubconnector. Private ci-state.json; do not redispatch.
  Previous CLIgh unavailable, existing authorizedconnector/browser used.
- NEW ace_fdt_copy_refusal_snapshot supports optional exact65536B opaque second
  chosen property ace,pmsg-before-seed, preserving original288B record ABI via
  NULL/0 wrapper. Full input/FDT/property/reserve preservation; output/snapshot/
  written aliases, badextent/duplicate/capacity refuse before stores. Four host
  FDTtestsPASS0.630s inclactual488KiBphoneFDT and all bytevalues/full64KiB.
  Pure normalRAM copier only, not physicalRAM ownership, collection or repair.
- Snapshot-copy API is NOT YET CALLED by native/Android/controller. Need capture
  whole failed-seed zone after existing ownership/exclusion gates without stores,
  then copy into refusalFDT, Android identity/currenttoken-bound readout of full
  property, hash/private persistence and QEMU end-to-end byte verification.
  Do not clear unknown data based on header/count alone or call snapshot API
  evidence of actual physical snapshot. Any later repair must preserve full
  evidence and be exact-hash/caller-owned/one-time gated, never blind reset.
- Since fdt_refusal source changed after observationcheck44213, NEW check17556
  LIVE rebuilds native+9preflights against same historical0113kernel under
  snapshot-codec-* dirs. Poll SAME17556; new result needed for current sources.
  This still does NOT test native snapshot capture (not integrated) or0114XNU.
- Latest connection-observation in ace-ufs-gpt-misc directory is fresh read-only
  expected product/B/unlocked/firmware Fastboot. INSTALLED remains full-readback
  verified2f5846...6dc4c6/token6ec5da258b9ff457, retained experiment; noADBscreen
  available in Fastboot. Previous screenshot is inspectedAndroidonly.
- NEXT poll17556 + CI39541641261 exactartifact/cachemetrics; integrate full
  evidence-preserving failedseed snapshot/readout before deciding actualRAM
  repair. Prepare fresh candidate from current SALVAGED/separate-return verified
  ancestry, not the older2b17control. No consumedcontroller/writer restart.
  ActualXNU0114GPT discovery/BSDroot/display/touch/usableiOS still UNACHIEVED;
  keep fullgoalACTIVE, no userdata overwrite/protected/GPT/slot/restore writes.

## ACTIVE HANDOFF: evidence-preserving pmsg observation + resilient Android log collection (2026-10-21)

- Previous goal turn PROGRESS: installed0113 actual normal refusal plus full
  identity/readback/salvage/automatic separate Fastboot return, realGPT81entry
  layout and local0114 exactmisc fix. Full usableiOS goal still ACTIVE.
- NEW controller root reads: refresh verified identity before EACH of <=4
  read-only attempts, retain every failed stdout/stderr/status/timeout with
  root-read-observations.json. Never fall back to stale transport. Actual
  TimeoutExpired partial output preserved. Essential token/root/B/fullboot/
  vendor checks still fatal. Optional Android pstore/dmesg/AEE log failure now
  recorded as incomplete and continues to the unchanged refreshed token-bound
  guarded reboot/Fastboot checks; RAM contract read requirements unchanged.
  Explicit log_collection_complete/diagnostics_complete flags prevent calling
  missing logs collected. No reboot retry policy weakened.
- Host20auto tests PASS0.015s incl failedpartial output/refreshedidentity/no
  identity no command/timeoutpartial and optional log fail followed by good
  guarded return vs mismatched token prevents ANY reboot. ThreeAEE tests PASS
  0.019s, three seedtestsPASS0.197s, pycompile/diffcheckPASS.
- New native seed-failure readonly observation: existing word23 retains first
  header8B (ACTUAL previous0113word23 was ZERO, not unknown); on seed<0 only,
  word25 now upper32=header.size/lower32=full64KiB nonzero byte count. Stage5/
  error-64/seed-3 context distinguishes observation from successful stage7
  branchflag1. Same seed/refusal/zone-preservation rules, NO clearing/repair.
  Prior actual zero first8 plus nonzero-refusal means unknown nonzero bytes
  elsewhere; does not establish size/body contents or authorize blind clear.
- Native host QEMUcheck44213 LIVE using HISTORICAL0113kernel201cfb...fd512,
  new native source, private ace-ufs-gpt-misc-20261021/observation-* outputs.
  Corrupt fixture now zeroheader + byte128=71; pmsg-refusal PASS, validates
  header0/count1/seed-3 and byteidentical ring/destination. Await all9cases.
  This is host native verification, not new0114kernel or phone evidence.
- 0114 published remote8f275b65eb96bf037d2833e4e860727e3afa5d6d on existing
  codex/ace-initial-platform (fresh prior branch verifiede634c41a...). Browser
  currently selecting cachedACE/diagnosticfalse form; NOT dispatched yet at
  this checkpoint. Do not confuse form with a createdrun. gh unavailable as
  verifiedprevious, existing authorizedconnector/logged-inEdge workflow used.
- Phone untouched THISturn: installed READBACKverified2f5846...6dc4c6 at firmware
  Fastboot after guarded separate return. No controller/writer restart or user
  actionpending. Next finish9nativecheck/commit, cached0114CI exactartifact,
  newnative/allpreflights, prepare from actual salvaged/separate-return ancestry.
  Next phone normalauto should decode originalheader/count if seed again refuses;
  do not claim pmsgfix, GPTXNUproof, BSDroot/display/touch/iOS yet.

## ACTIVE HANDOFF: 0113 trial refused before XNU; real GPT quirk fixed locally0114 (2026-10-21)

- INSTALLED/ACTUAL FULL READBACK verified boot_b
  2f584669f14a00d8e3b7e721dd659573ca028dbaebe34ae8795611c74c6dc4c6,
  token6ec5da258b9ff457. vendorbb5a09...9670/root/B/fullboot verified in
  android-stable.txt. Retained experimental image, NO original restoration.
- Writer24695rc0. Wrapper/controller18394 TERMINALrc1: diagnosticADB30.1s,
  actual288B currenttoken record stage5/error-64, word19pmsgcodec-3 and word31
  seed-3. THIS candidate did NOT enter XNU/materialize/read new GPT array.
  Earlier0112 XNU/UFS proofs remain historical, not this trial's result.
  Complete normal refusal Android boot is physically observed; pmsg corrupt/
  unknown nonzero refusal, original contents NOT established. Do not assumezero
  or blindly clear unknown RAM. Exact current error is the next native blocker.
- Controller failed with root evidence collection failed AFTER fullreadback,
  before screenshot/pstore; it recorded no individual failed-read stderr, so
  reason UNKNOWN. Controller/writer/wrapper never restarted. Separate read-only
  salvage22447rc0 verified serial+exactrecord before every read, saved empty
  pstore tar1536B, dmesg2548878B, AEE16202752B, screenshot and readstatuses.
  First salvage attempt used WRONG diagnostic property path and stopped before
  evidence/phone mutation; retained empty salvage dir, corrected salvage1 is
  authoritative. Screenshot INSPECTED: Androidlockscreen with wirelessdebugging/
  USBfunction dialogs, never XNU/iOS screen/touch proof. No manual user action.
- Separate guarded return74592 TERMINALrc0: one retained current288B readmatch,
  one ADB reboot rc0; productk6895v1_64/B/unlockedyes/is-userspaceno physically
  verified. Statephase diagnostics-salvaged-separate-return-fastboot-ready,
  separate_return_verifiedtrue, automatic_loop_verifiedfalse. Keep original
  controller failure distinct. Current actual phone is firmware Fastboot.
- During identity/currenttoken-bound Android salvage read exactly24576B from
  /dev/block/sdc (primary GPT, first6x4096 ONLY, no write), SHA
  43318ec9fadd317eb7face67f8f50bf6134d743947aae53de688b314cc42bdd5.
  HeaderCRCfedaebac/arrayCRC b989cbd8,81used entries, no GUIDduplicates/overlap.
  Actual misc index0 range8..135 attr0 lies below declaredfirstusable34; this
  was the sole initial hostparser -3, NOTzero uniqueGUIDs. userdata index79
  first3514368 blocks58961912 =>241507991552B. These are ANDROID reference
  reads parsed locally, NOT currentXNUhardware root discovery.
- NEW0114 + hostheader: allow ONLY observed misc index0/name exactUTF16+zero
  tail/8..135/attr0/capacitylast62480383/headerfirstusable34 exception; still
  fullCRC/uniqueGUID/nooverlap/otherpartitionbounds, exactuserdata boundselection.
  Five GPT/actualpatchedmethod tests PASS1.410s incl shifted/renamed/attribute/
  index exceptions refused. Real Android array parser now PASS/expectedbounds.
  Six ACE/SWEET Mach-O compiles PASS, SWEET code/data/relocations unchanged,
  all imports matchactualkernel ABI. Private ace-ufs-gpt-misc-20261021 outputs.
  0114 NOT published/CIbuilt/phonewritten yet. Preserve0113 acceptedCI/artifacts.
- NEXT: fix established pmsg-invalid pre-XNU gate with evidence-preserving
  diagnosis (record originalheader/seed decision, no blind clearing) and improve
  controller failed-read observations/guarded return after nonessential log
  collection failure. Do not restart consumed control/writer. Then0114 cachedCI,
  newnative/currenttoken/allpreflights/exactartifact and normalauto trial to
  establish actual XNU fullGPT/bounds. After that serialized BSDread/root bridge.
  No userdata overwrite until independent no-data recovery exists. Protected
  partitions/GPT/backups intact. Full usable iOS goal ACTIVE and UNACHIEVED.

## ACTIVE HANDOFF: 0113 GPT candidate installed; automatic trial LIVE (2026-10-21)

- Guarded writer24695 TERMINALrc0, one boot_b64MiB write accepted:
  Sending1.385s/Writing0.157s/total1.549s. INSTALLED NOW candidate
  2f584669f14a00d8e3b7e721dd659573ca028dbaebe34ae8795611c74c6dc4c6,
  token6ec5da258b9ff457; ACKNOWLEDGEMENT ONLY, readback pending.
  Priorverified2b17control remains last verified ancestry, not currentinstall.
- Wrapper18394 LIVE, USB observer confirmed ready BEFORE automatic controller
  started ONCE. Exact private research/ace-ufs-root-gpt-20261021/phone-trial
  controller-launch.json has processPID/timestamps. Poll SAME18394; never rerun
  writer, wrapper or controller. Expected Android-v1 ADB budget150s; verify
  currenttoken/root/B/fullboot+vendor, screenshot inspect, pmsg/dmesg/AEE and
  refreshed guarded firmwareFastboot return. Need real GPT CRC/bounds log.
- No otherpartition/slot/GPT/userdata/protected writes/restore. No manual action
  pending. This is genuine XNU storage discovery experiment, NOT iOS success.

## ACTIVE HANDOFF: 0113 GPT candidate validated; guarded phone write NEXT (2026-10-21)

- Local34245fd exact native canonical rootprofile +3a860d4 host policy; linked
  XNU201cfb...fd512 from successful cachedCI39539129481/job119022579305 remains.
  Final native/preflight63349 TERMINALrc0:9entry cases incl pending-latch refusal,
  actual first arm_init C instruction,5Android refusal paths incl durable handoff.
- Private research/ace-ufs-root-gpt-20261021 final64MiB boot candidate SHA
  2f584669f14a00d8e3b7e721dd659573ca028dbaebe34ae8795611c74c6dc4c6,
  fresh token6ec5da258b9ff457, native77594624B SHA
  9e84cf4a5a69f96cd35fec8fa5eef85fbfc5c406cf7f7ab88c5374ae205eb4a5.
  Originalgeneric54961de2...fa90d2, exact Android8d555b...f11d0 retained.
  Packaging rechecked full extracted image, kernelCI/ADT/SHA/source/reports/dumps/
  original boot+vendor backups. Root ADT is explicit discovery only, no BSD media.
- Fresh prepare26699 ran once; writer/ledger from actual verified2b17control,
  priorfullboot/vendor/root/B evidence pinned and newtoken absent prior evidence.
  NEXT execute write-gpt-once.py ONCE after its final identity/geometry/hash
  gates, then run-auto-once.py ONCE (USBmonitor ready BEFORE controller reboot).
  Wrapper saves controller-launch.json, terminates observer after controller
  terminal; no monitoring reboot/write retry. Controller itself preserves its
  refreshed current-token/identity/return guards and screenshot collection.
- At this checkpoint NO new phone write yet; installed verified2b17 control.
  No manual action pending, no protected/GPT/userdata/slot/restore operation.
  Need actual logs+inspect screenshot before claiming new hardware result.

## ACTIVE HANDOFF: 0113 CI accepted; fresh native checks running (2026-10-21)

- Mainline storage milestone local0fc93ea/handoffa24b833; remotee634c41a...90eae.
  CI39539129481/job119022579305 TERMINAL SUCCESS, cached build248s,
  nativeCCACHE1071hits/1miss, source/KDK+compiler caches genuinely restored.
  Artifact12319795009 ZIP73a532eab377f744ab6873ca8577dda2d748146255d56d5fc27e286885d48ed1.
  Actual linked kernel17541848B SHA201cfb1e222aa927dc0139929179268047087d4d270394df30892488b01fd512.
  Exact successful remote provenance/ZIP SHA/SHA256SUMS/entry+GPT strings/symbols/
  cachemaintenance disassembly accepted; private ci-job.log/accepted-provenance.
- First native packaging refused BEFORE directory/device mutation: mkpayload's
  strict ADT policy had not yet accepted0113. Fixed host policy with explicit
  boolean/requires-command-read/patch-list checks AND actual ADT node property
  agreement. Eight payload tests PASS1.585s incl mismatched/missing properties.
  No kernel/sourceCI change caused by this host-only fix, no new CI needed.
- Build-and-check84910 TERMINALrc1: first native built, QEMU pmsg-refusal
  stopped EARLIER at stage4/error-45 because native canonical ADT checker lacked
  the new exact property. No phone operation. Preserve native/preflight under
  *-rejected-platform-profile with logs; these bytes MUST NOT be phone trialed.
  Added exact canonical profile3 (same verified UFS hardware gates), property
  count/value/order still byte-for-byte; 12 native platform tests PASS5.365s.
  Fresh build-and-check63349 LIVE, NEW token/native, await9+Centry+5refusal.
  No kernel CI change needed; this changes only the native loader source.
  No phone mutation yet, installed VERIFIED2b17ee...90ac58 remains firmwareFastboot.
  Root-discovery2976B ADT already generated from pinned actual FDT.
- Private package-candidate.py/prepare-once.py prepared for0113 normal Android
  generic route; prepare script NOT executed. After checks, inspect exact package,
  prepare one-time writer/previousreadback+newtokenabsence pins, final firmware
  identity/backups/fullhash and one boot_b write, automatic controller ONCE.
  Do not use old paired-control native-token-only constraint for new XNU/ADT.
  GPT discovery is not BSD media/rootfs/iOS. No userdata/protected/GPT writes.

## ACTIVE HANDOFF: back on UFS/BSD-root mainline, 0113 ready for cached CI (2026-10-21)

- User explicitly prioritizes actual iOS boot on Ace. Continue storage/root
  bring-up using physically proven original-generic automatic trial route;
  RAM-only rescue remains unfinished and must be fixed before userdata overwrite.
  No claim that diagnostic Android or root bounds equal iOS success.
- Prior b22e161 adds optional read-only budget callback per <=64KiB rescue hash
  chunk/final pre-store gate; cancellation leaves input/output unchanged. Six
  initrd tests passed; older QEMU artifact predates callback, not retested there.
- NEW 0113 + ace/ufs_root_gpt.h: persistent singleton keeps controller/DMA/GPT
  state off kernel stack, refuses another owner and quarantines any negative
  command result. Explicit ADT --ufs-read --ufs-root enables ONLY four additional
  READ10 commands LUN2/LBA2..5/4096B after capacity-bound primary header CRC and
  exact observed 92B/v1.0/128x128 geometry. Complete 16KiB array CRC, used-entry
  bounds/unique GUID/no-overlap, exact UTF16LE userdata name/unique match checked.
  Output unchanged on refusal; no filesystem/media/BSD publication or disk writes.
- Actual prior Android header parser PASS: reference63ad1b...ca9d6, last62480383,
  usable34..62480375, expected entry-array CRCb989cbd8. Actual disk GUID is ZERO:
  removed unsupported nonzero-disk-GUID assumption before publication; disk GUID
  is not used for partition selection. Full real entry array not yet captured.
- Local five GPT/actual patched-method tests PASS1.216s; 15 ADT tests PASS0.836s.
  59 combined UFS tests PASS24.779s after final zero-disk-GUID relaxation.
  Six actual ACE/SWEET Mach-O single-file compiles PASS, SWEET code/data/relocations
  unchanged, all imports found in real linked kernel ABI. Private current outputs
  research/ace-ufs-root-gpt-20261021, exact patch applies fuzz0/header byteidentical.
- CI repository UnrealXu/ios-sweet branchcodex/ace-initial-platform currently
  a24fad106133e8a818d94186dcd6ba59093edfcf. Remote existing workflow/all patches
  blob hashes match local exactly. gh remains unauthenticated (attempted); use
  existing authorized GitHub connector + logged-in Edge for cached/diagnosticfalse
  dispatch, as previous iterations. Local0fc93ea/remotee634c41a60a68d0a8b6fd6508ed01eb461c90eae.
  CI39539129481/job119022579305 dispatched ONCE cached/diagnosticfalse, LIVE.
  Do not redispatch. Actual root-discovery ADT2976B generated from pinned FDT.
  UTC03:33:26 expected product/B/unlocked/firmwareFastboot freshly verified.
- INSTALLED remains verified normal-auto control2b17ee...90ac58/token9932497624433f86,
  no current-turn phone write/reboot/restore. Next publish0113, cached ACE CI,
  exact artifact/native/root-ADT checks, fresh token, one guarded boot_b write
  and automatic readout. First hardware target: complete GPT CRC + exact userdata
  bounds. Then implement serialized BSD read bridge/root device; neither is done.
  Keep Android userdata intact until independent recovery exists. Full goal ACTIVE.

## ACTIVE HANDOFF: initrd rewrite + bounded rescue codecs implemented, NOT integrated (2026-10-21 11:10 CST)

- Prior goal continuation interrupted intentionally during source/layout inspection;
  no process or phone operation was started there. New evidence: historical real
  FDT source68c811...560b initrdstart66f00000/end69509a70 =>39885424B versus pinned
  vendor38456840+originalgeneric1427884=39884724B, extra700B. Contents UNKNOWN,
  possible firmware bootconfig; never assume bare concatenation or call this a
  decoded actualfooter. This turn PROGRESS: tested executable rescue foundations.
- Source6a6e749 adds ace/initrd_rescue.[ch], ace/pstore_rescue.[ch],10new tests.
  initrdcodec requires explicit vendor/generic offset/size/SHA256 and rescueSHA,
  disjointsource/output/policy, shorter-or-equalreplacement, bounded64MiB extent.
  Full pin/footer/checksum/zeroalignment checks BEFORE any input/resultstore.
  Dryrunreadonly, refusalunchanged. Vendor and full bootconfig suffix preserved;
  adjusts zero padding to preserve footer alignment. No physical RAM ownership,
  FDTedit, native integration, partitionwrite or reboot in these helpers.
- Host5initrd tests PASS0.266s incl96 randomlength/alignment cases and truncation/
  alias/hash/footer/checksum negatives. Actual pinned streams + SYNTHETIC config
  verify-artifacts.py50599 TERMINALrc0, old47256543/new39884811B, vendor/rescue/
  configbyteidentical,guardretained/dryrunreadonly. OutputSHA
  c8ad909fa0ffc28efdb65c5116786552fd51c7a5d5d6371fa1f035cce92a0759.
- Exact ARM64codec compiledwith nativeflags/no undefinedimports. Individual
  .su frames112/208/320B. QEMU23214 TERMINALrc0 actualcodec under pinnedAndroid
  kernel, actualstreaminputs/syntheticconfig, outputhashMATCH/powerdown PASS.
  It does NOT boot Android from changed initrd or prove physical rescue.
- Rescue selector read-only states0oneRAM/1rescue/2stop from exact currenttoken
  armed + complete normalhandoff + complete rescue envelope with word31
  RESCUE01(3130455543534552). No initialization, duplicates/order/truncation/
  stale/textspoof refuse. Rescue selection append allowed once in state1 only,
  not repeated. FivehostlatchtestsPASS0.260s. Realretained currentcontrolpacket
  recognized protocolstate1, inputunchanged; originalcontrolNOTRAMtrial, so
  this is protocolcodec validation only. ARM64latch objectcompiled successfully.
- 123 focusedtests43523 TERMINALrc0/13.272s incl5initrd, plus5latch separately;
  128distinct tests PASS, not a claimed single128testrun. pycompile/diffcheckPASS.
  All localbuild/QEMU/testhandles terminal. No newCI, phonewrite/reboot/restore.
- Fresh UTC03:10:28 expectedFastboot present, private rescue-codec connection
  observation. INSTALLED remains VERIFIED control2b17ee...90ac58/token9932497624433f86.
  Fastboot has no ADB screenshot. No newuseraction pending; keep fullgoalACTIVE.
- NEXT integration required before ANY RAMhardwaretrial: embed pinned original
  generic with optional native rescue config; pin newcodec/SHA sources; validate
  actualFDTinitrd ordinarybank/reservation/image/FDT exclusions BEFORE reading
  or writing it. Read-only dryrun control should establish actualvendor/generic
  offsets and firmware bootconfig from current FDT; historical700B is insufficient.
  Add immutable-source FDTcopy/end-update preflight, then once-only rescue
  selection and actual RAM rewrite (consume selection before irreversible
  branch/mutation, preserve errors as attempt notsuccess). Never retryRAM in
  ambiguous/selected state. Default featuredisabled; readout-only pmsg unchanged.
- PID1fatal currentlyPOWER_OFF stays unchanged UNTIL matching embedded rescue
  capability gates warmrestart; never unconditionalrestartloops. Controller
  must explicitly distinguish Androidrescue from RAMsuccess while keeping
  currenttoken/serial/root/B/fullboot+vendor/refrreshedguardedreturn checks.
  Androidrescue depends on/data and is NOT diskless readiness or iOS success.
  NativeImagewindow, samekernel entry/Centry/refusalchecks, hostnegativecases
  and controlled multi-reset behavior still to validate. Native/API physical
  ownership and actualwarmreset safety remain UNPROVEN. No protected/GPT/data
  writes authorized beyond standing scope. FulliOS/display/touch/root/basic
  operations remainsunachieved; current work is necessary diagnostic recovery.

## ACTIVE HANDOFF: paired control fully automatic; RAM rescue still unfinished (2026-10-21)

- Control68012 TERMINALrc0, diagnosticADB76.1s/current9932497624433f86/root/B/
  fullboot_b2b17ee...90ac58/vendorbb5a09...9670 verified. One retained288B
  return-token observation matched; one ADB rebootrc0, expected physical firmware
  Fastboot verified. automatic_loop_verifiedtrue, ios_usablefalse. INSTALLED
  readback-verified control2b17ee490950ec29faf3fc0c88d52f72fee3c00b10deb75d3999904f7a90ac58
  RETAINED. No restore/protected/GPT/userdata/slot write. Sourcee7c65ae; prior
  handoffs178f770/8da920c/3ceb4e6 record RAMfailure/control write. No newCI.
- Screenshot saved/INSPECTED: Androidlockscreen withUSBselectiondialog, notiOS.
  USBmonitor93616 TERMINALrc124 after175s,25 kernelUSBevents; started BEFORE
  controlreboot. Controller/writer/monitor/AEE6249 allterminal, no live waits.
- New handoff marker PHYSICALLY observed once; appended288B envelope EXACTLY
  equals ADBreadout. Livepmsg18030B SHAfc8e36a5709edc9cb43d59fc410bea54b358aef27d09172b48e6fb86a19e933c.
  Current HWT db.fatal.01 SHA2b4b46c4217dfdd2bb97310f71938b574e3eba2e7cc18ab30f087e646ebebd2f,
  55entries CRC/size. All4archives240entries valid. HWT pre-reset17695B ring +
  exact335B post-reset handoff packet == livepmsg. NOT byteidenticalwithout
  suffix. analysis/control-conclusion.json captures scope. No9838priorRAMtoken
  in anyarchive/livepmsg; retentionloss/manualreset/earlierfailure not resolved.
- User instruction strengthened: fix automation so routine manual keys are not
  required. Control worksautomatically, RAM path still NOT FIXED. Nativebinary
  difference from RAMtrace is fresh token ONLY; originalgeneric versus RAMgeneric
  is controlledenvironmentdifference, individualfailurestage stillUNKNOWN.
- ESTABLISHED SOURCE GAP: preinit.fail() uses LinuxPOWER_OFF, so any earlyfatal
  cannot automatically return. Not proof phone took thisbranch. DO NOT merely
  change torestart and create unbounded loops. No further RAMhardwarecandidate
  until a bounded automatic rescue path is validated; preserve current healthy
  Fastboot/control image while doing offline work. No new permission required
  within standing boot_b/normalauto scope; do not re-request routine keys.
- NEXT implement bounded native+PID1 rescue design: retain currenttoken pending
  Android-handoff marker; after one RAM handoff, a subsequent warm reset selects
  pinned originalgeneric rescue instead of rerunning RAM. FatalPID1 restart must
  be enabled ONLY with matching native rescue capability (otherwise retain
  existing behavior). Preserve evidence and original vendor/bootconfig; label
  Android rescue explicitly, verify currenttoken/root/B/fullhash and guarded
  automaticFastboot in controller. Android rescue is NOT independent of/data
  and does NOT satisfy RAM/diskless/iOS milestones; actual RAMfailure must then
  be diagnosed/fixed from rescued logs before userdataoverwrite.
- FEASIBILITY ONLY: originalgeneric1427884B, RAMgeneric8799617B, native77594624B
  versus0x4e00000limit. Embedded originalgeneric appears size-feasible, and it
  fits in replaced RAMgeneric region, but safe runtime initrd surgery UNPROVEN.
  Need exact firmware initrd stream boundaries and checksum/bootconfig parsing,
  full source hash/range/ownership/exclusion checks before RAM writes; never
  modifyprotectedpartitions/GPT or assume bootloader fragment concatenation.
  Build/QEMU adversarialcases and controlledwarmreset/timeout/return tests first.
- This resumed turn PROGRESS (PID1trace + actualfailedRAM + physicallyverified
  pairedautomaticcontrol/newboundarytrace). Full iOS/display/touch/root/basic
  operations objective remains UNACHIEVED. No current user action pending.

## ACTIVE HANDOFF: user demands automatic recovery; original-generic control flashed (2026-10-21)

- User explicitly restored Fastboot again and asks to fix automation so routine
  manual operation is unnecessary. Fresh expected firmware/product/B/unlocked/
  is-userspaceno verified, private android-control0/user-restored-fastboot.json.
  This steers ongoing full iOS goal; automatic RAM log/readout/Fastboot remains
  a required prerequisite, not something already fixed by these diagnostics.
- Normal-auto Android-generic CONTROL prepared, no new diagnostic-only exception.
  Exact native bytes differ from failed RAMtrace native ONLY by fresh16hex token,
  byte-for-byte normalize comparison PASS. Same linked XNU/ADT/native code/pinned
  Android, original Magisk generic replaces RAM generic; wrapper remains new
  experiment, NOT original boot restore. One controlled XNU run is intentional.
- Native24392rc0, preflight75261rc0 all9 inclpending, C-entry60617rc0 firstarm_init,
  refusal98098rc0 all5 inclrealfallback/synthetic durablemarker. Same actual0112
  CI run39429611804/job118650915354, no newCI. package93707rc0, full64MiB SHA
  2b17ee490950ec29faf3fc0c88d52f72fee3c00b10deb75d3999904f7a90ac58,
  token9932497624433f86, originalgeneric54961de2...fa90d2. All current sources/
  reports/dumps/artifacts/full extraction/backup/kernel provenance passed.
- Private prepare76401rc0 pins pairedRAM failure plus actual forensic lastreadback,
  entire historical evidence and tokenabsence. Last installed163trace ACKONLY
  stays separate from lastverifiedbbcforensic; no false automatic_loop claim.
  Guarded normal-control writer6993 TERMINALrc0, one boot_b64MiB accepted
  Sending1.385s/Writing0.149s/total1.536s. Installed NOW2b17ee...90ac58,
  write acknowledgement ONLY pending readback. No otherpartition/slot/data/GPT/
  protected writes/restore. Writer consumed NEVER rerun.
- USB monitor93616 (175s) began BEFORE normal reboot; controller68012 started
  ONCE, normalAndroid150s ADB budget. Poll exact live handles; don't restart on
  observation timeout. Need retainedprior9838 token nativehandoff/PID1 traces
  in pstore/AEE, current9932/root/B/fullboot/vendor identity, screenshot inspect,
  guarded firmwareFastboot return. This control may isolate ramdisk difference;
  success is not RAM recovery/iOS/display/touch/root proof. Further fixes must
  follow actual logs, not guessed kernel/module changes or repeated lostUSB tests.

## ACTIVE HANDOFF: trace RAM trial timed out; paired Android control preparation next (2026-10-21 10:40 CST)

- Controller2629 TERMINALrc1 after240s noADB. Phase no-adb-after-240s-no-retry.
  No currenttoken/root/boot/vendor readback, screenshot, RAM trace, pstore/AEE or
  ADB return command obtained. Writer36294 consumed and controller NEVER restart.
  INSTALLED retained trace163bfc89...20119a/token9838a9120670e737, write ack ONLY.
- HostUSBmonitor48952 TERMINALrc124 expected245s; no kernel USB events during
  observed interval (started after normal reboot, NOT initial transition).
  UTC02:40:42 freshADB/Fastboot rc0 expected phone absent, stored private
  phone-trial2-trace/controller-terminal-observation.json. Failure stage still
  UNKNOWN; no evidence new persisted markers did/didnot execute on phone.
- New next strategy is a controlled normal-auto Android generic comparison,
  NOT another RAM retry or diagnostic-only flag exception. Same linked XNU,
  same instrumented native code, newtoken/pmsg/init-empty/auto-readout/pinned
  Android, original Magisk generic instead of RAM generic. This normal workflow
  remains within standing scope and collects retained prior RAMtrial traces
  plus its own XNU logs if readout returns. It does add one controlled XNU run;
  never claim skipped-XNU forensic recovery or RAM success. Experimental full
  image differs original backup; no routine restore.
- New private android-control0 native build started, poll actual handle in tool
  results. Then require9native/Centry/5fallback validation and full64MiB image/
  backup/source/artifact/provenance checks, fresh token absent prior records.
  No write until expected phone physically returns to firmwareFastboot and
  new reviewed candidate/guardedone-timewriter is ready. Manual assistance is
  now last resort because observed physical USB channel lost after real240s.
  Protected/GPT/userdata/backups untouched; full iOS goal remainsunachieved.

## ACTIVE HANDOFF: trace candidate flashed once; automatic controller live (2026-10-21)

- Source/PID1/QEMU/fullcandidate milestone committede7c65ae. Private offline
  prepare-trace-once.py38681 TERMINALrc0: validates actual forensic stage2/-66,
  explicit diagnostic-only scope/onecurrenttoken guardedreturn, root/B/fullboot/
  vendor readback, historicalmanifest/image/artifact/pstore/AEE pins and newtoken
  absence across prior forensic evidence. Preserves old automatic_loopfalse;
  no historical source replay/current-source bypass. New ledger TRUE current
  readbackbbc23a...59201b, unlike prior failed RAM acknowledged-only images.
- New phone-trial2-trace hostcontract/source/fullcandidate/ancestry/writer pins
  verified. Writer36294 TERMINALrc0; one boot_b64MiB flash accepted:
  Sending1.385s/Writing0.134s/total1.520s. New INSTALLED experiment SHA
  163bfc89c45430a1deb03322a14cfb8a4c0153f7c047ac9a48e2440d7320119a,
  token9838a9120670e737. Acknowledgement ONLY; no root/full readback yet.
  Firmware identity/product/B/unlocked/is-userspaceno/bootability/geometry and
  originalboot+vendorbackups checked. No slot/data/protected/GPT/restore write.
- Writer consumed NEVER rerun. Normal auto controller started ONCE on fresh
  phone-trial2-trace; poll live handle from tool result, maximum240s RAM budget.
  No forensic-mode exception applies/needed for this normalauto candidate.
  Need actual logs/screencap inspection if ADB returns; no assumed RAM success.
  Preserve experimental image on failure, never blindretry consumed controller.

## ACTIVE HANDOFF: PID1 pmsg trace and full trace candidate validated (2026-10-21)

- Previousfcb3ffa native instrumentation turn PROGRESS; this turn PROGRESS:
  optional token-bound PID1 trace implemented, actual kernel pmsg rings observed
  in controlled QEMU, matching physical ramdisk/fullboot packaged. No phone
  writes/reboots yet this turn. INSTALLED remains forensicbbc23a...59201b.
- preinit reads exact16hex+LF ramdisk trace-token, exactsysfs pmsg0/dev parser
  dynamicmajor1..4095/minor0. Creates0600privateRAMnode, duplicatesfd>=3+CLOEXEC,
  traces beforestdio AFTER virtual /dev/proc/sys mounts. Mirrors text/numeric
  output while preinit lives; errors disable optional trace only. Does not
  cover failure before virtual mounts or prove Linux on absent trace. No/data.
  New pmsg_trace.h pinned in base reports; physical trace-token hashed.
- pid1-trace0/99776 TERMINALrc1 due verifier GDB virtualmemory read after MMU,
  NOT boot failure. Retained serial shows actual pmsg active/stockinit/probe.
  Corrected pid1-trace1/25370 TERMINALrc0, all3 actual-kernel/full-vendor cases:
  normal and no-console realRAMring token+prestdio+secondstage records PASS;
  no-pmsg case trace unavailable but stockinit/adbd/probe/poweroff PASS.
  Synthetic QEMU pstore/token, no phone proof. Physical pmemsave used.
- Authenticated ADB/fullvendor/no-console84787 TERMINALrc0 PASS;118 focused
  tests73749 TERMINALrc0/11.248s,2new dynamicdevice parser tests; pycompile/
  diffcheckPASS. Native9+C-entry+5refusal validations retained priorfcb3ffa.
- physical-trace0 assembly17479rc0, token9838a9120670e737, genericSHA
  a364e216bb73f8c52f84e5de5f92f2736b54a7f8deca6645b6fd4d87f43acbc3;
  combinedinitrd3f79644106581b281e2975b4f029d5cd0d25d4f0f83a18c45e541765de3bdbce.
  Initial builder raw ~/.android pub pin differed ONLY newline; use pinned
  physical-host-adb.pub which equals currenthostkey after singleLF normalization.
  No key replacement/auth weakening.48module/returnfirst3/90s unchanged.
- candidate-trace0/experimental-ramdiag-boot-b.img64MiB SHA
  163bfc89c45430a1deb03322a14cfb8a4c0153f7c047ac9a48e2440d7320119a,
  package19602 TERMINALrc0. Sameactual0112 linkedkernel, noCI. Native source,
  9entry/Centry/5fallback report, allsource/artifact/report/dump pins, wholeImage
  extraction/exactgeneric/tracetoken validated. Never flash native Image alone.
- NEXT prepare fresh ledger/writer from ACTUAL verified forensic readback:
  priorforensic state diagnostic_only_return_verifiedtrue/automatic_loopfalse,
  root/B/fullboot+vendor/one guardedphysicalFastboot return proven. Existing
  generic prepare expects automatic_looptrue; do NOT forge this flag or reuse
  stale actual0112 as current. Validate historical artifacts as historical,
  keep current source pins/newtoken absent, then guarded boot_bonce/controlleronce.
  Standing normalauto trial authorization applies, no perwrite question needed.
  GoalfulliOS display/touch/root/basicoperations remainsunachieved.

## ACTIVE HANDOFF: durable pending Android boundary implemented/validated (2026-10-21 10:25 CST)

- Previous resumed turn was PROGRESS: real forensic readout/AEE/watchdog
  cross-check5ac9124. This turn also PROGRESS: native boundary instrumentation
  implemented and executed offline, no new phone writes/reboots/restores.
- ace/pstore_handoff.h writes one token-bound ACEANDROID1 pending-handoff marker
  plus exact288B envelope ONLY for valid current pending ring/stage5/-67/zero
  fallbackguard. No unknown-header seeding, malformed/stale records refuse
  without writes. Actual caller after CPU/exclusions/FDTcopy, compiled only
  pmsg+auto&&!diagnostic. Append best-effort/no changes to record or return path;
  diagnostic-only mode still writes nothing. Marker means branch prepared only,
  absence remains inconclusive; neither means Linux/PID1/iOS success.
- Native helper header pinned by mknative. verify_refusal adds explicitly
  synthetic pending-handoff fixture: real fallbackcode writes exact packet,
  unchanged Android boots and guest FDT record matches. Other4cases pstore
  unchanged. RAMcandidate package now requires5cases/3guestreadbacks/2guards
  and durable_handoff_record_verified + synthetic flag, never hardware proof.
- New private native-handofftrace0/native Image77594624B SHA
  450fd5a59749d8df7b2d15cc8239367975b85c1da2eb77cb2de0726ec45e5ea1,
  token9838a9120670e737, pmsg/init-empty/auto/pinnedAndroid/textoffset0.
  Same kernel3846d1...d366, actual0112 CI39429611804/job118650915354;
  no new CI. Native92733rc0; fallback6041rc0 all5PASS; preflight12550rc0
  all9PASS inclpendinglatch/phonePA; C-entry69428rc0 actualfirstarm_initPASS.
  Host116 focusedtests78841rc0/10.001s, includes19pstoretests/3newcodec tests;
  final actual5case report shape checked after guest-count package update.
  pycompile/diffcheckPASS. All processes terminal; no live handle waiting.
- Fresh read-only UTC02:24:48 expected firmware Fastboot/is-userspaceno still
  present. New token absent from296 prior forensic evidencefiles, observation
  native-handofftrace0/read-only-observation.json. INSTALLED remains VERIFIED
  forensicbbc23a...59201b, originalbackups intact. No ADB screenshot while
  firmwareFastboot. Prior native/forensic manifests are historical now that
  source changed; never replay old writers/controllers or bypass their pins.
- NEXT finish earliest RAMPID1 stage tracing (independent of console availability,
  no persistent mount; establish actual pmsg-device availability rather than
  assuming it). Then rebuild physical ramdisk matching newtoken and current
  source, controlled exactkernel/vendoroverlay QEMU including no-console path;
  package fullboot with newnative5case report/current sourcepins and recovered
  forensic readback ancestry. Prepare guarded one-time write, fresh physical
  identity/backup/hash, automatic controller once under standing authorization.
  Do NOT flash native Image alone or mismatched old physical profile. No
  userdata overwrite before diskless path proven. Full iOS goal unachieved.

## ACTIVE HANDOFF: cross-checked real consolefix XNU/watchdog evidence (2026-10-21)

- Forensic controller8509 and offline AEE75960 TERMINALrc0. Private analysis/
  cross-check.json: exactly one archive contains b6cf74b8748e4e4e, HWT SHA
  ac3169f3c5ffc68a5ea9a91b788c8c63ec8e72c5b43654334dcc066b11c91ad9.
  All four archived records decoded, all240 ZIP entries CRC+size checked
  (75+55+55+55); current HWT55entries. Pstore ring35390B byteidentical to
  separately collected pmsg SHA105c3945faae74183efec5290c50dbce7b18c672499f4b38bf256cb12dfe7637.
- Actual consolefix-token XNU segment SHA89a831a1bc90f8e0470a205a1cc11f8eae26f82afd29ef81ff106b4f8de4e838:
  Darwin22.6 banner, BSDinit/setconf, real boundedUFS capacity/GPT blocks0/1
  complete. Firmware watchdog at38.15s, sampledPCfffffe0007491a9c resolves
  exactlinkedkernel to _cpu_idle+0x1ec. No panic/CPUfault/rootmount diagnosis
  inferred from idle PC. No recovered RAM LinuxPID1/module/USB receipts.
- docs/ACE-RAM-DIAGNOSTICS.md current status corrected (earlier sections retain
  historical chronology). Installed/readback-verified forensicbbc23a...59201b;
  automatic diagnostic-only return ready, firmware Fastboot retained, no restore.
- NEXT concrete investigation: instrument durable native Android handoff and
  earliest RAM PID1 stages to locate missing automatic RAM readout, with exact
  kernel/physicalFDT/ramdisk controlled validation. Stock config confirms
  PSTORE/PSTORE_CONSOLE/PSTORE_PMSG/PSTORE_RAM=y, but this alone proves no runtime
  trace availability. No guessed fault fix or blind repeat is justified by
  current logs. Preserve original backups/latest experiment/protected/GPT;
  no userdata overwrite before physical diskless diagnostic path is proved.
- Meaningful hardware/evidence PROGRESS this resumed turn, no approval pending
  for the completed forensic operation. Full usable-iOS/display/touch/root and
  basic operation objective still unachieved. No live process left to wait on.

## ACTIVE HANDOFF: real forensic readout and automatic Fastboot return succeeded (2026-10-21 10:14 CST)

- Controller8509 TERMINALrc0. Expected diagnostic ADB26.1s; fresh token
  d2e7d2345169cdc7/root/B/full64MiBboot_b bbc23a...59201b/vendor bb5a09...9670
  VERIFIED. Installed forensic image retained and now readback-verified.
- Readout stage2/error-66 is EXPECTED diagnostic-only skip, automatic_pending
  false/automatic_loop_verifiedfalse; diagnostic_only_return_verifiedtrue.
  Prior b6cf74b8748e4e4e marker observed once, validring0/offset18063; 35017
  prior nonzero bytes. Marker alone never iOS success. Full actual pstore35390B
  recovered includes prior trial0 and consolefix XNU logs through genuine UFS
  capacity/GPT blocks0/1 completion. No RAM PID1/module/USB success proven yet.
- pstore/dmesg/AEE saved; AEEattempt0 complete16217088B SHA
  f1a1133f590bc4395a3a6975c6b6a1d98c778114a98512e83be14a0c6f58aaba.
  Android screenshot saved/visually INSPECTED: entirely black, no visible UI;
  SHA b2c02d7c3c068af916e428b862fa1f18ab99e6b8c4948cbc8e8f68a9988314d1.
  This is Android diagnostic capture, NOT XNU display or iOS proof.
- One retained288B/currenttoken return observation matched; one return reboot
  rc0, no retry. Physical firmware Fastboot product/B/unlocked/is-userspaceno
  verified by controller. No restore/protected/GPT/slot/userdata flashing.
- Current offline AEE decoding session75960 live; poll SAME handle, no restart.
  New private analysis/decode-aee.py validates every ZIP entry CRC/size and
  searches archive token to distinguish current/old records. Need inspect logs
  before selecting next established fix. Goal user resumed, work proceeds;
  no complete claim. Source/handoffc9dcd3b precedes this success.

## ACTIVE HANDOFF: forensic exception approved; one write succeeded (2026-10-21)

- Human replied to explicit diagnostic-only exception request: "现在进入fastboot了
  请你继续". Contextual approval recorded privately with fresh firmware identity:
  expected serial/productk6895v1_64/B/unlockedyes/is-userspaceno verified.
- New forensic writer24585 TERMINALrc0, single boot_b64MiB write accepted:
  Sending1.390s/Writing0.134s/total1.526s. Full source/artifact/image/backups/
  prior-failure tokenabsence/physical identity/partition checks passed. New
  INSTALLED forensic SHA bbc23a912ff31c89c164ab1613209b046bd5560fc73af7ef69310e495d59201b,
  tokend2e7d2345169cdc7/priorb6cf74b8748e4e4e. Acknowledgement ONLY, no readback yet.
  No original restore/userdata/protected/GPT/slot write. Writer consumed NEVER rerun.
- Controller started ONCE with --diagnostic-readout-only/private transport/new
  forensic-consolefix0/phone-trial. Next poll live session from tool result;
  preserve observations and inspect any verifiedADB screenshot/logs. Do not
  repeat writer/controller. Readout skips XNU and preserves native pmsg;
  neither entry marker nor Android screenshot proves iOS. Full goal unachieved.

## BLOCKED AUDIT: no physical USB or diagnostic exception reply (2026-10-21 09:45 CST)

- Previous continuation041756e was NO PROGRESS, not a live-process verified wait.
  Revalidated current state UTC01:45:01: ADB/Fastboot commands both rc0 but
  expected phone absent; diagnostic exception authorization remainsFALSE.
  Evidence pending-forensic-recheck2-20261021T014501371488Z/observation.json.
- Same genuine blocker observed in three consecutive goal turns: actual consolefix
  failure/forensic preparation turn, first01:44 continuation, second01:45
  continuation. First turn made source/package progress; those independent
  authorized preparations are now complete, tested and committed. No recovered
  phone logs establish another implementation fault; no live process to wait on.
- Cannot meaningfully proceed with hardware diagnosis without recovered USB and
  human reply to the specific diagnostic workflow exception. No new phone write,
  reboot, consumed controller restart, backup restoration or authorization change.
  Mark goal BLOCKED after committing this handoff, not complete or paused.
  Full iOS/display/touch/storage/basic-operation objective remains unachieved.
- Resume from prepared forensic candidatebbc23a...59201b, writer and trial ONLY
  after explicit diagnostic exception approval and freshly verified firmware
  Fastboot. Latest installed consolefix684e61...b8184 remains retained; original
  backups intact. Follow detailed handoff below, never repeat consumed trials.

## PENDING EXCEPTION RECHECK (2026-10-21 09:44 CST)

- Previous goal turn was PROGRESS: real single consolefix write/240s terminal
  readout failure plus tested/pinned forensic package and controller changes
  1bfa6f4/handoff59691fc. This continuation is NO PROGRESS toward hardware bring-up:
  no new explicit human exception approval or recovered phone transport.
- Fresh UTC01:44:27 ADB/Fastboot commands rc0, expected phone absent. Private
  evidence pending-forensic-check-20261021T014427511205Z/observation.json.
  Offline full forensic source/artifact/image pins revalidated; persisted
  authorization false/phase awaiting-workflow-exception-and-firmware-fastboot.
  No commands writing/rebooting phone, controller restart or restoration.
- No live build/controller/monitor wait; prior handles terminal. Await explicit
  diagnostic-only exception reply and physical firmware USB. Do not treat an
  automatic goal continuation as approval. Same blocker first continuation after
  progress; below three-consecutive-goal-turn threshold, goal remains ACTIVE.

## ACTIVE HANDOFF: consolefix automatic readout failed; forensic exception pending (2026-10-21 09:43 CST)

- User restored firmware Fastboot at09:25; 0545c54 records identity/preflight,
  6010290 records single guarded consolefix boot_b write. Writer56290 rc0,
  Sending65536KB1.386s/Writing0.157s/total1.545s. Acknowledgement ONLY, no
  full partition readback. INSTALLED remains64MiB SHA
  684e61c25af6f19b6153e1161d26e67ef955f1d9f63eb5db0c9bcd233e6b8184,
  tokenb6cf74b8748e4e4e. No original restore, slot/userdata/protected/GPT write.
- Controller15979 executed ONCE; normal Fastboot reboot accepted0.051s.
  TERMINALrc1 after240s, phase no-adb-after-240s-no-retry. No diagnostic ADB,
  token/root/boot/vendor readback, pstore/dmesg/AEE, screenshot or automatic
  return command. NEVER restart consumed writer/controller. Phone stage UNKNOWN;
  console defect remains independently reproduced, physical failure cause unproved.
- Private phone-trial1-consolefix/controller-terminal-observation.json records
  failure. Host USB monitor92497 endedrc124 after260s, header only/no events
  DURING observed interval; began after initial reboot, not complete boot coverage.
  Fresh UTC01:42:55 ADB/Fastboot inventories contain no expected phone; stored
  forensic-consolefix0/phone-trial/connection-recheck.json. No verified ADB means
  screencap unavailable. Manual assistance remains required if USB stays absent.
- Prepared diagnostic-only forensic candidate, NOT written/authorized:
  research/ace-ramdiag-20261020/forensic-consolefix0/boot-candidate/
  experimental-forensic-boot-b.img SHA
  bbc23a912ff31c89c164ab1613209b046bd5560fc73af7ef69310e495d59201b,
  fresh tokend2e7d2345169cdc7, priorb6cf74b8748e4e4e. Same linked kernel
  3846d1...d366/run39429611804/job118650915354, NO new CI. Native --pmsg
  --diagnostic-readout --prior-run-token, pinned Android8d555...f11d0;
  deliberately NO pmsg initialization and NO XNU attempt/auto-readout flag.
  Original Magisk generic diagnostic ramdisk, NOT original boot-image restore.
  Android services may write normal runtime logs; no userdata flashing proposed.
- Five QEMU forensic cases PASS, three guest record readbacks, one explicitly
  synthetic prior marker fixture; every pstore-before equals pstore-after.
  Build/verification46985rc0, packaging94568rc0. Full64MiB/native/embeddedAndroid/
  source/artifact/provenance/backup pins and prior evidence tokenabsence checked.
  Offline copied-state validator PASS; persisted authorization remainsFALSE.
- New private forensic-consolefix0/write-forensic-once.py prepared/syntaxchecked,
  NOT executed. Requires explicit workflow exception AND write auth, selfpin,
  fresh manifest/source/artifact/backups/previous-failed-state/phone identity,
  firmware B/unlocked/product/is-userspaceno/bootability/exact64MiB geometry.
  Consumes latch BEFORE sole boot_b flash, no automatic write retry/rollback.
- Public controller supports explicit --diagnostic-readout-only ONLY with
  diagnostic_only_exception_authorized=true and source/artifact-pinned manifest.
  Preserves prior entry interpretation as marker only, never iOS success.
  Normal trials still require auto-readout. Android return SU observations now
  retain each rc/stdout/stderr/partial timeout with no hidden inner read retries;
  existing maximum3 refreshed identity-bound read guard/reboot constraints remain.
  RAM candidate pins include imported forensic validator. 97 focused tests
  PASS8.945s, pycompile/diffcheck PASS. Source changes committed1bfa6f4.
- APPROVAL NEEDED specifically for one diagnostic workflow exception, NOT routine
  per-write permission: AGENTS.md requires --auto-readout-after-reset for candidates,
  but tools/ace-mknative.py diagnostic-readout is explicitly mutually exclusive.
  Need human exception approval before changing false authorization or executing
  forensic writer/controller, plus fresh physical firmware Fastboot if absent.
  Pending state phase awaiting-workflow-exception-and-firmware-fastboot.
- NEXT after explicit approval + verified firmware USB: authorize prepared fresh
  forensic state with reply basis, execute writer ONCE then ace-auto-trial.py with
  private transport/trial and --diagnostic-readout-only ONCE. Verify currenttoken,
  root/B/fullboot/vendor, save/inspect Android screenshot and actual logs, guarded
  return to firmware Fastboot. Retained prior marker is not iOS proof. Preserve
  all evidence/backups/latest experiment. No blind repetition on further failure.
  Goal ACTIVE after user resume; full usable-iOS/XNU display/touch/root unachieved.

## ACTIVE HANDOFF: consolefix flashed once; automatic readout next (2026-10-21)

- Guarded consolefix writer56290 terminalrc0. Sending65536KB OKAY1.386s,
  Writingboot_b OKAY0.157s, total1.545s. All source/artifact/image/backup/ancestry/
  device/partition/bootability checks passed before flash. One boot_b only, no
  slot/data/protected writes/reboot/restore yet. Acknowledgement, NOT readback.
- INSTALLED now full64MiB consolefix SHA
  684e61c25af6f19b6153e1161d26e67ef955f1d9f63eb5db0c9bcd233e6b8184,
  tokenb6cf74b8748e4e4e. phone-trial1-consolefix statecandidate-flashed-awaiting-reboot,
  flashsuccess true. New writer consumed, NEVER rerun. Old failed trial0 retained.
- NEXT automatic controller once with phone-trial1-consolefix and privatetransport,
  240s RAM budget. Preserve every observation; no blind write/reboot/oldcontroller
  retry; inspect real evidence/screen if verifiedADB appears. Firmware currently
  confirmed before nextnormalreboot. Native/iOS/physical RAM loop unproven.

## ACTIVE HANDOFF: user restored firmware Fastboot; consolefix trial proceeding (2026-10-21 09:25 CST)

- User explicitly reports Fastboot restored and asks to continue. Fresh expected
  serial/productk6895v1_64/B/unlocked/is-userspaceno verified at UTC2026-10-21
  01:25:47, phone-trial1-consolefix/resumed-connection.json. Goal active again;
  previous blocker resolved. Firmware Fastboot has no ADB screencap capability.
- Installed remains failed b53be406...933fad8b until next guarded writer succeeds.
  New consolefix684e61...b8184/tokenb6cf74b8748e4e4e prepared, writer/state selfpin
  match and fresh/empty write ledger. Do not rerun oldtrial0 writer/controller.
- NEXT execute write-consolefix-once.py ONCE (all package/source/backup/ancestry/
  partition/device checks), record actual result, then auto-trial ONCE. Keep
  experimental image; no routine restore or protected/data/slot writes. Old
  failure has no recovered logs; new revision fixes independently reproduced
  console dependency, physical cause/success still unproven.

## CURRENT CONNECTION RECHECK: user-requested check (2026-10-21 04:13 CST)

- User asked whether the phone is available now. Fresh read-only observation
  research/ace-ramdiag-20261020/user-connection-check-20261020T201304Z at
  UTC2026-10-20T20:13:04: Fastboot inventory empty, ADB inventory empty, host
  USB inventory contains no phone. No identity-verified transport/screencap.
  This does not prove the phone's visible mode; screen/cable state unknown.
- No write/reboot/controller/writer restart/restore. Installed failed b53be4...fad8b
  and queued consolefix684e61...b8184 remain unchanged. Asked user for current
  screen mode and to check connection to this computer. No new blocked-status
  call; this is the first user-triggered recheck after prior blocked audit.

## ACTIVE HANDOFF: console-fix boot candidate ready; physical USB blocks next step (2026-10-21)

- Candidate/ledger/tests/handoff committed b55cce5. Previous console-fix
  milestone f3ec4b8/handoffa97b555 was PROGRESS. This turn
  is PROGRESS: matching fresh native Image/preflights/fullboot packaging and
  correct failed-install ancestry/state ready. No new phone write/reboot/
  controller execution/restore. Full usable-iOS goal remains unachieved.
- INSTALLED remains failed experiment b53be40604ab70d8a08ac5c9bafde63bfc49f94c70c03846c5939f48933fad8b,
  tokena95b5e377195d1ac. Do not restart consumed phone-trial0 writer/controller.
  Root/partition readback for this installed image STILL UNAVAILABLE. Last actual
  readback remains actual0112 aab18c...24d4. Source-level console defect verified
  by controlled QEMU, actual phone failure causal diagnosis still unproven.
- Fresh source-bound native-consolefix0 Image
  c9dda82827fb49ca81da83551585742f1b8a5c8237001ec8bf2f0289cfcdfdd9,
  77594624B, tokenb6cf74b8748e4e4e matches physical-consolefix0. Same pinned
  actual0112 linked CI kernel3846d1...d366/run39429611804/job118650915354,
  no new CI/native/XNU implementation change. pmsg/init-empty/auto-readout/exact
  Android8d555...f11d0 pins intact. Nine cases inclpendinglatch/C-entry/four
  refusal preflights all PASS, native11632 terminalrc0.
- Full64MiB candidate-consolefix0/experimental-ramdiag-boot-b.img SHA
  684e61c25af6f19b6153e1161d26e67ef955f1d9f63eb5db0c9bcd233e6b8184.
  Generic0426c3...86c8b4. Current source/artifact/report/dump/archive pins verified,
  extracted native/generic match; original AVB bytes retained/relocated with NO
  validity claim. Candidate NEVER flashed/executed. Packaging76696 terminalrc0.
- Public prepare helper now optionally accepts acknowledged failed install
  separately from last verified trial. It checks one boot_b write/rc0/OKAY,
  terminalnoadb240/controller1/no restart/no readback, oldmanifest pin/full64MiB
  image/all historical artifacts, exact previous-verified-state ancestry and
  tokenabsence in both evidence sets. Rejects replay same image/token, ambiguous
  flash, active controller, wrongpartition, modified/broken ancestry/evidence.
  Historical source is never replayed/accepted as current newcandidate source.
  Actual old candidate source now obsolete, retained bytes/logs ONLY evidence.
- phone-trial1-consolefix prepared, fresh partition_writes_startedempty, explicit
  RAM contract/source pins/newcandidate. last_verified_boot_b_sha256=aab18c...24d4;
  previous_boot_b_sha256=b53be4...fad8b; previous_install_readback_verifiedfalse.
  previous_evidence_sha256 pins old failed records, last_verified_trial_state
  pin remains historical successful loop. Private write-consolefix-once.py
  self-pin stored. Before any mutation it rechecks ALL new sources/artifacts,
  bothoriginalbackups, bothledgers, hostcontract and exactfirmware serial/
  product/B/unlocked/bootability/partition/maxdownload. physical_connection flag
  currentlyfalse; only fresh passedpreflight may settrue. Writer NOT executed.
  Prepared body does NOT authorize replaying failed writer/controller.
- All91 focused RAM/controller/AEE/stockchain/nativeimage tests PASS11.442s,
  includes5 new failure/replay/ancestry ledger guards; pycompile/diffcheck PASS.
  All native/build/package/prepare/test handles terminal; NO live wait process.
- USB blocker same three consecutive goal turns: initial actual240s readout
  failure/finalnoUSB at17:27; consolefix turn freshnoUSB17:29/17:37; this turn
  followup-consolefix2 UTC17:44:22 and newtrial connection-observation UTC2026-10-20
  17:52:11 both adb/fastboot commandsrc0, expectedserialabsent. No identity-verified
  ADB, screencap unavailable. Manual Fastboot action requested earlier, no human
  completion/response observed. Never infer returned USB from state files.
- BLOCKED AUDIT: independent established console fix, real same-kernel QEMU
  validation, freshramdisk/native/fullcandidate and newledger/guardedwriter work
  now completed. Next meaningful hardware action requires actual phone USB to
  return. No further established source fault can be chosen from absent logs.
  Threshold three consecutive goal turns satisfied; mark goal blocked after
  final connection recheck/commit if still absent, not complete or paused.
- RESUME when phone returns: freshly verify expected serial +firmware product
  k6895v1_64/B/unlocked/is-userspaceno, collect/inspect screenshot if verifiedADB.
  Preserve old records and original backups; recover earlier pstore/logs where
  possible and review forensic implications before next experiment. New fixed
  candidate/standalone writer available under standing authorization; use only
  concretehashes, consume one writer/controller ONCE if proceeding. No fastboot
  boot/oldcontroller restart/blind retries/routine original restore/ userdata
  write. Physical consolefix/module/UDC/UFS/firmware loop and iOS remain UNPROVEN.

## ACTIVE HANDOFF: console bootstrap defect reproduced/fixed; phone still absent (2026-10-21)

- Implementation, reproduction evidence and rebuilt ramdisks committed f3ec4b8.
  Previous native RAM trial/package ab0fed4/write93b6f29/failurehandoff4baadb8 was
  PROGRESS. This turn makes independent source/runtime progress while waiting
  for manual Fastboot: establishes and fixes unavailable-console bootstrap
  failure. Physical failure causal diagnosis remains UNPROVEN without logs.
- NO new phone write/reboot/controller run/restore. Still installed boot_b
  b53be40604ab70d8a08ac5c9bafde63bfc49f94c70c03846c5939f48933fad8b,
  tokena95b5e377195d1ac. phone-trial0 remains no-adb-after-240s-no-retry. Both
  consumed writer/controller MUST NOT restart. Fresh read-only followup1 at
  UTC17:29:15 and console-fix-current-observation.json UTC2026-10-20T17:37:13:
  noexpectedADB/noexpectedFastboot, commandsrc0. No verifiedADB, no screenshot
  possible. Original backups unchanged. Manual response still pending.
- console-hardware-audit.json: pinned live FDT68c811...560b chosen bootargs have
  console=tty0 twice; pinned stock kernel CONFIG_VTdisabled, 8250runtime0,
  MT6577UART=m. Old preinit unconditionally opens /dev/console before modules;
  inability triggers fail/poweroff before stockinit. Phone's actual Linux entry,
  open errno/poweroff NOT observed; don't call the hardware cause established.
- New preinit standard_io keeps successful-console path. Only ENODEV/ENXIO/EIO
  falls back to RAM/dev/null stdin +/dev/kmsg stdout/stderr; any unexpected path/
  permission error/fallback failure remains fatal. Short marker proves branch.
  No persistent access or weakened RAM/B/policy/native/module/UFS/USB checks.
- QEMU console-unavailable-baseline0 old ELF rc0 EXPECTED REFUSAL: consolewarning,
  powerdown, NO stockinit. Tty0-specific baseline-final0 repeats with matched
  hardware bootarg. Most rigorous console-identical-overlay-old-init0 uses the
  final successful USB/fullvendor fixture but replaces ONLY init with preserved
  old ELF95a2708064ea0f593eb54e4459b86caf8d70e60f0e1118ec0eb1f0bc0f2d10af.
  All other archive entries +originalvendor prefix identical; rc0 earlypoweroff
  beforestockinit. SerialSHA
  882c93e71f11acc67cca65c56da6b9b188ce55abd8e4ee42a8a1f1135f2c755c.
- Actual fixed console-tty0-usb-fixed-final0 rc0 PASS: explicit fallbackmarker,
  stockinit/root/no_data/policy/virtualmounts, secure wrong/trustedkey USB auth,
  exact8192B binary and one hostpoweroff; initialFFsbindtimeoutfalse. SerialSHA
  93b14c7d99936dadd90bd9da4931d232aa603bc58f5396b9f179ae1c4c33f183;
  genericSHA c3326b110bbfc0882799f4890e2c7a49d5358ff7fc4532d63c5e2e2b54012a6e.
  Normal-console USB/fulloverlay regression rc0 PASS serialSHA
  97ee959cbcb2628681617529afae776cb37da67797c660d26429ea1cf779513d.
  First fixed0 fixture failed because cat large procstatus to kmsg hit record
  limits; retained as harnessfailure, not PID1failure (root/adbd alreadyseen).
  Isolated QEMU probe now rawttyAMA0 for those dumps; physicalpayload contains
  NO probe/UARTfixture. Early printk only does NOT supply a console tty.
- Fresh physical-consolefix0/1 actualserial/key48module assemblies compiled
  only, all53 comparedpayloads identical; physical-consolefix-reproducibility.json.
  New tokenb6cf74b8748e4e4e, absent in ALL retained failed RAMtrial0 and oldactual0112
  files (not a fresh phone read). GenericSHA
  0426c3cb3a4461a62697d43c0a1b98dfa44c5a366c62b6f2b3641827f586c8b4;
  combinedSHA1d22fdf19a0b4b0a7a54a8893a201cfc2e5a5f3944b3d92807993d3da6faa2fc.
  NOT native/boot candidates yet, NEVER flashed/executed physical48bundle.
  Old physical-build5/candidate-physical1 source pins now intentionally obsolete
  against changed preinit/qemu helper: preserve them as installed-artifact
  evidence, never edit manifests or rerun oldwriter to bypass source checks.
- All86 focused RAM/controller/AEE/stockchain/nativeimage tests PASS7.526s;
  pycompile/diffcheck/real crosscompiles PASS. All build/QEMU/test handles terminal.
  No new XNU kernel/CI change; goal active, real iOS/display/touch/rootfs incomplete.
- NEXT offline: rebuild native Image using SAME newphysical token from
  physical-consolefix-input.json and pinned actual0112 kernel/ADT; rerun9case/
  C-entry/4fallback preflights, package new64MiB native+consolefixgeneric. Existing
  prepare helper requires prior SUCCESSFUL loop, so do NOT feed failedtrial0
  as if it were successful; represent last verified readback vs acknowledged
  failed installed write separately when preparing next trial. Obtain fresh
  exactserial/product/B/unlocked/is-userspaceno after user's manual Fastboot
  recovery; inspect/recover actual failure logs when possible. No blind retry,
  unsupported fastboot boot, routine backup restoration or userdata changes.

## ACTIVE HANDOFF: first physical RAM readout FAILED; manual Fastboot needed (2026-10-21)

- Code/package milestone ab0fed4; acknowledged write checkpoint93b6f29. This
  goal turn is PROGRESS: real experiment changed installed boot and established
  a physical readout failure. Usable iOS goal remains active/incomplete. No
  confirmed source fault yet; do NOT guess a module fix without recovering logs.
- INSTALLED/retain experiment boot_b full64MiB SHA
  b53be40604ab70d8a08ac5c9bafde63bfc49f94c70c03846c5939f48933fad8b,
  native tokena95b5e377195d1ac, genericSHAae461535...130ce. One guarded write rc0,
  Fastboot sending1.389s/writing0.146s/total1.537s, acknowledged not independent
  partition readback. One normal fastboot reboot accepted rc0/0.052s. No other
  phone write/reboot/slot/GPT command, no backup restoration. Original backups
  were full-hash verified before write. No host userdata write command issued;
  physical RAM root/no_data state was NOT observed after this boot.
- tools/ace-auto-trial.py executed ONCE, source-pinned RAM contract. Actual
  session80351 terminalrc1 after full240s: no-adb-after-240s-no-retry. It did NOT
  reach record/root/partition/hash/log collection or return-reboot command.
  writer13703 and native93530/test54907/package/prepare handles all terminal.
  Do NOT restart either consumed writer/controller or blindly repeat flash.
- phone-trial0/normal-reboot.log, flash-candidate.log, state.json,
  controller-terminal-observation.json retain exact results. Waiting hostsysfs
  observation UTC17:25:34 matched NO expected USB serial; ADB list empty.
  Final after-timeout-observation.json UTC2026-10-20T17:27:00: ADBnoexpectedserial,
  firmwareFastbootnoexpectedserial (emptyFastboot list), rc0 inventorycommands.
  Phone has no identity-verified ADB: no screencap possible. No native288B record,
  pstore/dmesg/AEE/full boot/vendor readback or visible iOS evidence available.
  Unknown whether native/firmware/RAM bootstrap/module/USB failed; NO diagnosis
  inferred from absent transport alone. Last successful firmware identity BEFORE
  reboot is retained in bootloader-preflight.json; not a current connection.
- User manually returning Ace to Fastboot was requested via async question,
  using the previously successful device-specific method. Reason: full bounded
  automatic trial failed, no software USB channel, AGENTS last-resort condition.
  No unsupported fastboot boot or repeated reboot attempted. Manual answer still
  pending at this checkpoint. Do not mark goal blocked on this first occurrence.
- NEXT: wait for/manual Fastboot restoration, then freshly verify exactserial/
  productk6895v1_64/B/unlocked/is-userspaceno, not state-file inference. Keep all
  RAM trial observations and original backups. Recover actual prior-trial logs
  through a concrete reviewed diagnostic path; avoid reattempting the same RAM
  boot without evidence. Existing diagnostic-only native readout tool supports
  prior-run-token, but is mutually exclusive with automatic XNU mode: review
  recovery-specific scope/provenance before using it. Never call an unmodified
  original restore routine or delete Android userdata here. iOS/rootfs/display/
  touch, physical RAM module/UDC/UFS/automatic firmware return remain unproven.

## ACTIVE HANDOFF: RAM candidate flashed once; automatic trial next (2026-10-21)

- Packaging/control source committed ab0fed4. Guarded private writer terminalrc0:
  Sending boot_b65536KB OKAY1.389s, Writing OKAY0.146s, total1.537s. One boot_b
  write only, no slot/protected/userdata writes, no restore/reboot yet. This is
  firmware write acknowledgement, NOT independent partition readback or boot.
- INSTALLED experiment now full64MiB SHA
  b53be40604ab70d8a08ac5c9bafde63bfc49f94c70c03846c5939f48933fad8b,
  tokena95b5e377195d1ac; replaces historical actual0112. State phone-trial0
  candidate-flashed-awaiting-reboot, candidate_flash_succeededtrue. Consumed
  write-ramdiag-once.py MUST NOT restart. Full image/backups/source/contract and
  firmwareproduct/B/unlocked/is-userspaceno/bootability/geometry passed before
  flash, retained at phone-trial0/bootloader-preflight.json +flash-candidate.log.
  Recovery remains original backups/verified firmware Fastboot path; no pending
  routine restore, retain experiment. Firmware presently before normal reboot.
- NEXT run tools/ace-auto-trial.py with existing private transport and phone-trial0
  ONCE, current RAM contract and240s bound. Do not rerun writer or fastboot boot.
  Native/physical RAM startup/return/iOS still UNPROVEN; inspect actual results.

## ACTIVE HANDOFF: native RAM candidate prepared; write pending (2026-10-21)

- Previous assembly milestone b11391e/handoff9dedcd2 was PROGRESS. Native Image
  and full64MiB RAM candidate now built/verified offline; one-time writer and
  explicit RAM controller contract prepared. NO write/reboot performed at this
  checkpoint. Historical installed actual0112 remains unchanged until writer
  succeeds. Last fresh Fastboot/B/unlocked/is-userspaceno observation remains
  physical-preparation-current0. Original backups intact; no userdata change.
- research/ace-ramdiag-20261020/native-physical0 uses original linked actual0112
  CI run39429611804/job118650915354 kernelSHA
  3846d1c7d547a256c2ad4cc77f12072475d8c7296fa9dac2e36dc74bdae8d366.
  No CI needed/dispatched. Same physical-build5 token a95b5e377195d1ac, pmsg,
  init-empty, auto-readout and hash-pinned exact Android8d555b...f11d0. Native
  cd72023f9c500c21ccf10a433f816534c0bfad8b8e88c32423b3eff94ce5a850,
  77594624B. Nine nativecases inclpendinglatch, actual C entry and four refusal
  cases PASS at preflight/c-entry/qemu-verified. Handles terminal.
- tools/ace-ram-candidate.py checks all source/report/dump/physical archive pins,
  CI provenance, exact embedded Android and token, then packages64MiB boot with
  explicitly pinned physical generic. Independent extraction verifies both
  native and generic bytes. Original obsolete AVB bytes relocated as existing
  boot path; no signature validity claim. Public helper NO phone commands.
- CURRENT candidate-physical1/experimental-ramdiag-boot-b.img SHA
  b53be40604ab70d8a08ac5c9bafde63bfc49f94c70c03846c5939f48933fad8b,
  67108864B. physical0 identical image but obsolete controller source pins;
  do NOT use its manifest. RAM controller now150+90s=240s ADB budget due known
  module supervisor stage; Android still150s, gates/retry rules unchanged.
- phone-trial0 prepared via source-bound helper with prior actual0112 physical
  readback/artifact hashes and token absence in ALL prior trial files checked.
  Host contractSHAef3af548828ebd0f2c0f170fdefc6efc8503f589862f03802e8a6dc648c0b89d.
  State readout_profileramdiag-v1, phasewrite-authorized-awaiting-final-bootloader-checks.
  Private write-ramdiag-once.py self-pin in state: validates whole package,
  backups/controller/contract/prior state, exact firmwareFastboot identity, slot,
  partition/maxdownload/bootability; records consumed state BEFORE one boot_b
  flash. No other partition/slot mutation/reboot, no repeat on failure.
- All86 focused RAM/auto-trial/AEE/stock-chain/native-image tests PASS8.401s.
  Pycompile/diffcheck PASS. Original kernel/native implementation unchanged;
  only fresh native token/diagnostic ramdisk packaging. iOS target incomplete.
- NEXT: standing-authorized execute private write-ramdiag-once.py ONCE after
  commit/checkpoint, inspect exact flash result and update installed state, then
  tools/ace-auto-trial.py with private transport JSON and phone-trial0 ONCE.
  No fastboot boot, no blind retry/controller restart. On ADB save/inspect
  screenshot (headless failure recorded), realnative record/partitions/logs,
  sourcepinned hostcontract and refreshedtoken guarded firmware return. Retain
  experiment. Full RAM physical module/UDC/UFS/return UNPROVEN before this trial.
  If no ADB, inspect actual transport/log state before any manual help request.

## ACTIVE HANDOFF: physical RAM ramdisk and current-native startup gate (2026-10-21)

- Implementation/tests/assembly evidence committed b11391e; this handoff
  records the exact milestone. Previous controller bcfafc2/handoff6477489 was
  PROGRESS. This turn
  assembles the actual serial/key-bound RAM ramdisk and native/physical startup
  gates. No partition write/reboot/CI; read-only phone discovery/getvars and
  backup hashes verified. Goal active: usable iOS/display/touch/rootfs unproven.
- FRESH physical-preparation-current0/observation.json at UTC2026-10-20T17:14:35
  (localOctober21) proves expected phone firmware Fastboot productk6895v1_64,
  current-slotb, unlockedyes, is-userspaceno. ADB absent; screencap unavailable
  in firmware Fastboot, explicitly recorded. Both original64MiB boot/vendor
  backups full SHA match. LAST installed boot_b hash remains HISTORICAL actual0112
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746. No subsequent writes, but no fresh partition hash read.
  Android userdata unchanged; no routine restoration. Protected partitions intact.
- New physical_assemble.py builds only a generic ramdisk/combined initrd offline,
  NOT a native/boot candidate or writer state. Revalidates pinned48 module plan,
  compiles real serial-bound return-prefix3/supervisor90s, copies original modules,
  creates actual key/profile/environment. Real48 module bundle NEVER executed.
  New native_gate.c validates root/RAM/no_data and actual chosen288B envelope
  with compiled current token, exact magic/padding/version/stage1..7/error-127..-1
  and zero handoff, then exclusively saves whole record in RAM. Normal refusal
  allowed alongside pending stage5/-67; these are errors, never iOS success.
- Physical init starts only one startup shell before adbd. Current native record
  precedes supervisor; exact return/completion receipts and fresh record compare
  follow. Real ueventd label aliases ONLY, full64MiB geometry/GPT numbers, unique
  block devnos/rdev/sysfs/uevent, exact112b0000.ufshci/logical4096, whole vendor
  hash and exactUDC11201000.usb0 required before readiness. Host later checks
  enclosing boot hash (avoid circular digest). Pstore explicitly mounted and
  actual PID1 mountinfo checked. TCP disabled. Native record checked again before
  readiness; one literal physical UDC bind on FunctionFS+readiness properties,
  attempted latch prevents rebinding. No persistent mount/write/reboot logic.
  Complete startup shell/actual module/UDC/UFS return remains UNEXECUTED/unproven.
- Original host adbkey.pub lacked final newline: initial build0 failed BEFORE
  output creation. Normalized private public-key copy RSA524B matched existing
  private-key derivation; originals unchanged. Kept build0 log/input privately.
  Subsequent prototype1/2 reproductions passed;3/4 added pstore; discarded these
  prototypes from next-action selection because current gate permits all valid
  normal refusal errors. No prototype was flashed. Input token checked absent
  from ALL historical actual0112 trial files, NOT fresh pretrial live evidence.
- CURRENT physical-build5 + physical-build6 independent assemblies: all53 compared
  payload files identical (generic/combined/native-gate +48modules+2ELFs).
  physical-reproducibility-current.json retained. GenericSHA
  ae46153531bf7268971588c25b48caefa3994132af265d5ce05ecefb1ca130ce;
  combinedSHA b8887176b7be46bd179e2e27e1d45132813de872f1c94f436e5d74fa134376ad;
  native-gateSHA9c8ccce7e2d8bf12b5e9d6925734f8e9f21149a9b1d74e271eadea26028bcd9e;
  real bundleID44dc45a18e9555782dc78103eddd75bd4071fb9f38131dd02130be3a8363a67a.
  Independent archive audit168entries/allmodes+hashes/48modules, original compressed
  vendor prefix byteidentical, delayedadbd/TCPoff/no dummyUDC, empty nonexec recovery.
  Every QEMU probe/proxy/fault/observer/workload asset excluded from finalpayload.
- Actual fixed-kernel native-gate-{pending,refusal,stale,oversize}-pstore-final1
  QEMU all rc0 PASS. Synthetic chosen DT records explicitly; NO physical proof.
  Pending and othernormalrefusal save exact288B actual sysfs data, second run
  refused without replacement. Stale/oversized create no checkpoint. Actual
  pstore mount, trusted/wrongkey secure root adbd, one hostpoweroff each verified.
  Final serialSHA pending887f877750a62ff4c3ccbf5d48dea4a56310a46e5e8fda63db967fdaecdaf7cb;
  refusal e3fd21041bae6d784420b49fe95e4e00269e7d59d8227f80752790568be7d16e;
  stale7908a8f400aad175e1fbf2b2eb84bf182a64e4de62fc4a5faa7f424794c564b8;
  oversize362eed88dd427bcb63a84bdfa32fc04da961a17babd6374c77aba714e7dd3626.
  Earlier native-gate prototype fixtures also retained; final1 includes current
  predicate and explicit pstore verification. All69 focused offline tests PASS
  0.794s, pycompile/shellsyntax/diffcheck PASS. All handles terminal; no native XNU
  source/kernel changes, no new CI run. No consumed physical controller restarted.
- NEXT CONCRETE: use current physical-build5 generic with SAME private native token
  from physical-build1-input.json/profile. Rebuild native Image from pinned
  actual0112 linked kernel/ADT with pmsg/init-empty/auto-readout/hash-pinned refusal
  Android. Re-run exact native9case/C-entry/4fallback preflights. Package64MiB
  boot_b with generic replacement using explicit ramdisk hash and validate all
  source/image/artifact pins. Generate ACE_RAMDIAG_HOST_V1 contract/source pins,
  extend guarded writer/preparation state to explicitramdiag-v1. Revalidate
  current device/backups/recovery and token absence from latest evidence; consume
  guarded write once then controller once under standing authorization. Firmware
  return physically UNPROVEN for this profile. Retain experimental image, inspect
  logs/screens if available; handle concrete early/module-stall failure with no
  blind writes/reboot/controller restart. No userdata write until physical
  independent no-data diagnostic loop passes.

## ACTIVE HANDOFF: pinned direct-root RAM readout controller (2026-10-21)

- Implementation/tests/evidence committed bcfafc2; this handoff records the
  exact milestone. RAM readout integration and tests; previous milestone
  code caa9c06/handoff5b11411. No phone I/O/write/reboot/screenshot/CI this turn.
  LAST VERIFIED installed boot_b remains actual0112 SHA256
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, historical firmwareFastboot/B/unlocked observation.
  Android userdata and original backups untouched; no silent restoration.
  No new physical XNU/iOS/display/touch/storage-write proof. Goal is PROGRESS,
  not achieved or blocked. Private artifacts remain research/ace-ramdiag-20261020.
- ace-auto-trial keeps default android-v1 behavior. Explicit ramdiag-v1 requires
  trial-relative pinned host contract BEFORE any reboot. Contract binds actual
  serial/native token/current boot/vendor/kernel/source hashes, module bundle,
  guest profile bytes and private GPT geometry; unknown profile/pin/path/extent
  failures stop without commands. Host vs guest profiles separate image hash
  from embedded context to avoid a circular digest. Actual writer does NOT yet
  produce RAM state/contracts; no physical RAM image assembled or flashed.
- RAM direct root uses sh exec-out, never su/sys.boot_completed/data-AEE. Every
  read refreshes expected serial identity, retains command/rc/stdout/stderr,
  preserves timeout partial bytes, adds NO generic retries. Fresh native288B
  record/token precedes nonce-bound snapshot/root/B/secure/no_data/virtualmounts,
  exact guest profile and both65B module/return receipts. Receipt is local flow
  identity, not physical success/remote attestation. AEE explicitly unavailable.
- Both boot/vendor full64MiB hashes require consistent block rdev/sysfs/uevent,
  GPT label/number/start/length, distinct devnos, exact112b0000.ufshci ancestry,
  logical4096. RAM screenshot attempted immediately after identity return; saves
  unavailable metadata when headless. No physical screenshot attempted this turn.
  Existing current-record3-read/complete-other-stop and one-command firmware
  return/exact-no-device-only retry remain. Final command-manifest digest is
  refreshed after token return observations. Existing Android branch preserved.
- Actual readout-command2 QEMU rc0 PASS complete64MiB commands via authenticated
  stock root adbd. Synthetic read-only USB GPT disk BOTH partitions128MiB total;
  fullbootSHA dbfaca2662cb70b69dfefd5ac95d1f54a73663092d46cefdc9609dc695a12c98,
  fullvendorSHA07a1e6f3b84e57fbffcbc20ed126f43ceeaec19b8a1cdc0e63b3a75421e6dc54.
  DiskSHA cf810a57083f5cbc6342726f207245889f20090674b4768d7397570f04dd3898.
  Correct distinct8:1/8:2/labels/GPT observed. Production validator explicitly
  rejects USB ancestry; no fake UFS acceptance. SerialSHA
  8f73ac34f24d60706633c85d9dd2890ed1b3fcf276e320a0e540d925bd281b46.
- Actual readout-usb-overlay-final0 QEMU rc0 PASS combines full original vendor
  overlay, secure USB FunctionFS trusted/wrong-key auth, exact8192B binary,
  both complete64MiB partition commands and one authenticated poweroff. RAM root
  virtual mounts/no_data verified. SerialSHA
  679162b40bde9e12e859660d2b5e6b8b30531ea5613d150a818839f9e91d3c9d;
  genericRamdiskSHA1cf4aa87b7aff4895480f4c0cfe6cbd1225b4a939e120c2ddd495fada2b072ee.
  This is component compatibility only, NOT physical USB/UFS/firmware reset or
  complete controller-native-record execution. No simulated record passed as
  hardware success. Main loop integration uses explicitly synthetic mocks.
- Retained failed readout-command0 established unquoted hash echo collapsed
  two spaces: fixed quoting, exact parser unchanged. Failed command1 established
  idle timeout during full hash. Opt-in QEMU fixture now90s total/30s idle,
  original default25s/5s unchanged; total capped120s. No physical timing relaxed.
  All65 focused RAM/auto-trial/AEE offline tests PASS0.646s, compile/diffcheck
  PASS. Earlier seven test errors came from manually constructed fake wire
  objects missing the new idle field; fixture fixed, all actual guards pass.
  All QEMU/build/test handles terminal. No native kernel change/CI necessary.
- NEXT CONCRETE: assemble actual physical RAM profile from pinned vendor with
  real serial/pinned existing host ADB key, exact11201000.usb0, real48 module
  bundle/supervisor/receipts and fresh token/pmsg/auto-readout. Generate matching
  guest/host contracts and extend guarded preparation/writer state with explicit
  RAM profile/source/image pins. Gate guest readiness on actual current native
  record and partition identity, not supervisor exit alone. Review current
  transport, concrete hashes/backup/recovery; use standing experimental boot_b
  authorization, consume guarded writer/controller once and retain experiment.
  Verify actual UDC/UFS/early return and firmware Fastboot with logs. Do not
  write userdata until independent no-data physical RAM loop passes. Handle
  established early/unreaped failure without blindly restarting or rebooting.

## ACTIVE HANDOFF: phased return initialization and one-child module supervision (2026-10-21)

- Implementation/tests/evidence documentation committed caa9c06; this handoff
  records the exact milestone. Private modules, generated headers and logs stay ignored.
- Previous binding/ABI turn f3cf804/68ec507 is PROGRESS. This turn implements
  return-first ordering, early binding checkpoint, exact completion receipts
  and a bounded one-child supervisor. No phone I/O/write/reboot/screenshot/CI.
  LAST VERIFIED installed boot_b remains actual0112 SHA256
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746; last verified firmwareFastboot/B/unlocked. Historical,
  not a current device observation. Android userdata/original backups untouched.
  No new physical XNU/iOS/display/touch/storage-write proof. Private artifacts
  continue under research/ace-ramdiag-20261020 despite current date21.
- Planner RETURN_PREFIX now forces mtk_wdt/reboot-mode/syscon-reboot-mode as
  first3, before ANY remaining45 modules; missing/nonclosed hard/pre ordering
  refused. New module-plan-phased0/report.json SHA
  aabd725df04c7b0edda6396eef017fa4218b8ef9f797084e7221cf168251b37e.
  Watchdog and reboot-mode contracts marked early. After first3 insertion and
  both actual OF/driver/module/DT checks, loader creates an exclusive RAM return
  checkpoint. Only then may later modules insert. Final non-early checks precede
  a separate completion receipt. ALL48 SHA/sealed copies still verified first.
  Checkpoints are binding evidence, not proof firmware reset/IRQ/UFS IO works.
- New module_supervisor.c starts fixed loader ONCE; root/nonPID1/RAM/no_data,
  no prior module/checkpoint/complete state and exclusive own latch required.
  Default full-bundle deadline90s, poll cap; child failures never restart. At
  expiry sends SIGKILL ONCE, waits at most5s/grace poll cap; exits124 if reaped,
  125 if still unreaped, never ready. A kernel-stalled child may not be killable;
  ordinary interruptible sleep was tested, NOT a hardware/kernel deadlock.
  No supervisor reboot, rollback, module unload or persistent operation exists.
  Existing token-refreshed ADB→Fastboot return rules remain unchanged.
- Child exit0 ALONE is refused. Parent requires an exact65B regular-file RAM
  completion receipt (64hex bundle identity + newline). Identity hashes serial,
  release/module bytes/order/gates/bindings/stage/deadline AND policy source
  hashes. Parent and child compile the same identity. Atomic latch prevents
  repeat child starts, including after timeout with no loader marker present.
  Receipt is a local control-flow identity check, not a cryptographic remote
  attestation or an iOS/hardware-ready marker.
- Full48 module-bundle-phased0/phased-rebuild0 compiled/bundled only, NEVER
  executed. All52 files identical (48modules/2ELFs/2headers), default90s and
  return_prefix_count3. BundleID
  9a4aa10a92466c4f093cbdf506f54354bf36068a88d5db458b692665dd839219;
  loaderSHA99927cc22f31eb165aa24c6cd4b0110e5967c5337943a97eec990873ebd3b138;
  supervisorSHA17fe2df15d0463126a0a32ccce1b56be5fb53853723287972b5db8f2676d8860.
  Reproducibility.json retained. Synthetic RAMDIAG_QEMU_FIXTURE serial only;
  no physical boot image generated. Production bundle NEVER includes module_fault.c.
- Actual supervisor-insert-final1 QEMU PASS/rc0: two original nonmatching stock
  modules inserted, actual PCI/builtin/reg/class early check passed; checkpoint
  appeared BEFORE second insertion. Exact completion receipt verified only after
  child0. Second invocation refused, exactly one child start. Same run passed
  secure authenticated root TCP/RAM receipt/ONE host poweroff/policy/no_data.
  RamdiskSHA6e56bc85ae2c95b4c6b7eb4f6f5615d3f2ae345011b4bb80957129e64d3d10b4;
  serialSHA15bdbf9054f75097ac2539463013a4c625f9971a133f8e581c1dd10cf5287698.
  This proves process/stage semantics, NOT physical return driver operation.
- Refusal fixtures all QEMUrc0 / PASS EXPECTED REFUSAL ONLY:
  supervisor-early-refusal0 wrong DT bytes→child1, parent1, no checkpoint and
  NO second insertion; retained first module. SerialSHA
  2e60dc089b267110cb96886b95fd553de4c89990e2aa9421f4edca95deafe105.
  supervisor-hash-refusal0 second file bad→no first insertion, child1/parent1;
  serialSHAac36cffc9066fb779a9ea4f3d2cf52599828ffe818fcceecab8ce9b15b5f6b5c.
  supervisor-hang-final1 explicit negative sleeper→1s test deadline, one kill,
  reaped/status124; second parent invocation EEXIST before any second child.
  SerialSHAe672b9d7ebea8b6be1dfe7942ec510c8770b0c480a89561f383708a8cabf4b52.
  supervisor-no-receipt0 and supervisor-wrong-receipt0 explicit negative stubs
  exit0 but parent refuses absent/incorrect receipt. SerialSHA respectively
  cc74694e07c65858ce0a39ca55d9b9239579fd43a8cd034d14659289908c6311 and
  e89225c1c383005713aabfe4047ca11be0d1a624e1e201fa45d615ddb51745b5.
  Faults substitute QEMU-only user executables, not genuine hardware failures.
- Direct unsupervised loader regression PASS/rc0, serialSHA
  f915188742b7e317b2db12cbd5dc87894069ccd6a307b8de20d982669ca4a79d.
  All37 RAMdiagnostic host tests PASS0.975s. Compile/diffcheck PASS. No broad
  kernel suite/CI needed; native XNU and pinned Android Image unchanged. All
  test/build/QEMU handles terminal; no consumed physical controller restarted.
- NEXT CONCRETE: implement direct-root RAM readout profile in ace-auto-trial
  (no su/sys.boot_completed/data-AEE assumption) and physical ramdisk assembly
  using real supervisor/bundle, exact11201000.usb0, pinned existing host ADB key,
  fresh native token/pmsg/auto-readout, current288B record, UFS partition/hash
  checks and one-command token-refreshed firmware return. Preserve old Android
  profile behavior and writer/source/image hashes. Supervisor success is only
  module completion; do not publish diagnostic-ready before token/partition
  identity checks. Keep early-failure evidence without unauthorized reboot or
  restart; unreaped kernel failures still need concrete recovery treatment.
  Physical module/UDC/UFS/return loop remains UNPROVEN. No userdata write until
  the independent no-data loop physically passes. Standing write authorization
  remains; do not re-ask per operation once concrete image/gates are prepared.

## ACTIVE HANDOFF: reset-return closure and runtime OF binding checks (2026-10-21)

- Code/tests/evidence documentation committed f3cf804; this handoff records the
  exact milestone. All private source downloads, modules and logs remain ignored.
- Previous USB turn a824a26/d055964 is PROGRESS. This turn adds the previously
  omitted reboot-mode/watchdog closure, a source-pinned runtime binding/DT
  property contract, and correct ARM64 open flags. No physical phone I/O/write/
  reboot/screenshot/CI. LAST physical state remains actual0112 boot_b SHA256
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, firmwareFastboot/B/unlocked. Historical, not fresh
  observation. Android userdata/backups intact. Work crossed midnight; private
  artifacts remain in the existing ace-ramdiag-20261020 directory deliberately.
  No new XNU/iOS userland, display, touch or persistent operation proof.
- Exact live FDT watchdog@1c007000/reboot-mode has syscon-reboot-mode,
  offset0x24/mask0xf/mode-bootloader3. Official source shows reboot-mode's named
  command notifier calls syscon regmap_update_bits; callback failure can merely
  log and notification still returns NOTIFY_DONE. Binding is NOT proof of a
  successful future MMIO mode write or physical Fastboot return.
- Planner now seeds that exact node as well as USB/UFS:68nodes/172provider edges/
  48modules, adding mtk_wdt.ko,reboot-mode.ko,syscon-reboot-mode.ko. Private
  module-plan-return0/report.json SHA256
  e15f8a1ce8e5bf492b20f5d742e1896badea8e396265ff483001cb2b4da341d9;
  module-plan-return-rebuild0 report byteidentical. Source observations include
  WDT restart priority128, HW_RUNNING detection and31s timeout init, not binary
  instruction-equivalence proof. Config HANDLE_BOOT_ENABLED=y/OPEN_TIMEOUT=0.
  Historical0112 Android dmesg independently logs mtk-wdt1c007000.watchdog:
  Watchdog enabled(timeout31,nowayout0). No new watchdog opened or hardware tested.
- binding_contract.json defines four exact OF path/driver/module checks for
  USB mtu3, UFS ufshcd-mtk, watchdog mtk-wdt and child syscon-reboot-mode.
  Physical USB additionally requires /sys/class/udc/11201000.usb0, never dummy.
  Builder verifies pinned source strings/macros (MTU3_DRIVER_NAME via mtu3.h),
  owning module metadata and exact FDT. Compiled expected reg/compatible and
  reboot offset/mask/mode bytes come from the pinned DT, not arbitrary runtime
  strings. Raw DT files remain private. Full source hashes/contract hash retained.
- Loader scans only real /sys/bus/platform/devices, bounded getdents/paths and
  unique OF-node target; checks driver and module symlinks, DT property bytes,
  then real sysfs class path. Missing/unbound is read-polled with nominal15s
  deadline/scan limits; a complete wrong identity fails immediately. Checks do
  no bind/unbind/register/MMIO/block writes. They still do NOT prove UFS LUN IO,
  power/IRQ/USB operation or automatic firmware return. Kernel probe itself can
  stall; a userspace deadline is not an overall hardware watchdog.
- New binding scan exposed an inherited ABI BUG: ARM64 O_DIRECTORY=040000 and
  O_NOFOLLOW=0100000, unlike earlier generic flags. Prior directory flag was
  O_DIRECT (open sysfs failedEINVAL); prior intended NOFOLLOW was O_LARGEFILE
  and did not enforce symlink refusal. Existing module/USB fixture inputs were
  ordinary nodes, so earlier successful loads did not prove NOFOLLOW. Corrected
  both loader and USB proxy through shared aarch64_flags.h, verified against
  ARM64 UAPI. Atomic O_CREAT|O_EXCL latch already refused existing symlinks, but
  its explicit flag is corrected too. No new RAM profile was ever flashed while
  those flags were wrong. Final symbolic-module fixture now genuinely getsELOOP40.
- Final binding-insert-final3 TERMINAL PASS/QEMUrc0: exact stock reset module
  inserted, actual PCI OF node /pcie@10000000 matched pci-host-generic/builtin,
  exact reg bytes+sysfs class verified; consumed latch refused second invocation.
  Same run authenticated root TCP/RAM receipt/one poweroff/policy/no_data passed.
  UART was an unsuitable initial fixture (AMBA, not platform bus); after fixing
  flags its OF scan correctly found no platform match. PCI fixture uses actual
  dumped virt FDT and pinned source driver name. Failed attempts0/1 retained.
  Final ramdiskSHA
  0f176f1e43f8c2fb2ee06f2968aa73cb85a2941c62212ab1abff6b7473c711c8;
  serialSHA8a4109ac569b010c4409353bc70c93ec5cc5941122ac4e6bca468438b52000f0.
- Negative fixtures TERMINAL PASS REFUSAL COMPONENTS ONLY, QEMUrc0:
  binding-symlink-final1 ELOOP-40 before insertion, serialSHA
  a4bf51b385cc57e9ea4793f9e1042f19379febdf0efef78de5c4f1263e137bd7;
  binding-missing-final2 deadline-110, retained reset module, serialSHA
  117d3bf2ea810a33643c857537f02a998ef30e00f7823614a7e5567b2c8179c8;
  binding-wrong-driver2 immediate-22, serialSHA
  5902a0a3ceec77e7a974cd62018f3052c5df05bf2138cd853e9a28d6baab8b8f;
  binding-wrong-module2 immediate-22, serialSHA
  2e441605699a903ad1e5e3c8383f8ecdfc1773c62b097261a1f643fb737696e7;
  binding-wrong-property2 exact-byte mismatch-22, serialSHA
  7b0c0d5333c8c9821349b071ea0bf421b2974bfcc9790a0fcc642f4261d41059.
  These prove refusal logic, not the physical four-device contract.
- USB proxy corrected-NOFOLLOW regression usb-auth-flags5 PASS/QEMUrc0/full
  vendor/real dummyUSB AUTH/root/8192B/one authenticated poweroff/no initial bind
  timeout. SerialSHA
  c5915a3cf589ae1da021b06fee292195b1e25aa6d0ac28c5524baddf063d80fd.
  All35 RAMdiagnostic host tests PASS1.091s, compile/diffcheckPASS. No broad CI.
- Full48 bundle module-bundle-bindings0/rebuild0 has four contracts and all50
  files byteidentical (48 original modules/header/loader), plan also identical.
  Full loaderSHA1e986d32de49d9b0679b3ee7982da464556c4d40183495e8654ef050e12da483;
  headerSHA2ce63f949f174d0f90e918b0051abb52486176a3ea29d40805e3f1af6f538a9c;
  contractSHA520c566bfba8792bc24417c522044581f3c2498443dbd0014b640243688cf36d.
  Reproducibility.json verifies bootloader offset/mask/value too. Synthetic
  RAMDIAG_QEMU_FIXTURE serial only. Full48 NEVER executed; no phone image built.
  All tool/QEMU/download/build handles terminal. Private new sources include
  WDT/reboot-mode/syscon, mtu3 source/header and PCI generic fixture driver.
- NEXT concrete work: assemble a physical RAM profile with the exact UDC,
  selected bundle and direct-root auto-readout controller preserving current
  native token/refusal record/pstore/full boot+vendor hashes/serial, plus its
  failure/recovery path and one-command firmware return. Account for return
  initialization order: current proposal puts mtk_wdt24,mtu325,reboot-mode35,
  syscon-reboot-mode41,TCPC44,extcon45,UFS47. It is NOT an accepted physical
  supervisor sequence; do not claim end-of-load binding checks protect earlier
  probe failures. Include reset-return readiness in supervisor design. Need
  actual UFS partition/hash readiness and controller profile, not just bindings.
  Keep fresh-token native/one-time writer/auto-return safeguards before any
  physical candidate. No userdata write until no-data diagnostic loop proven.

## ACTIVE HANDOFF: stock adbd authenticated over real in-guest USB endpoints (2026-10-20)

- Implementation/tests/evidence documentation committed a824a26; this handoff
  records the exact milestone. Private keys, vendor bytes and logs stay ignored.
- Previous sealed-loader turn fea03bd/fae566b is PROGRESS. This turn adds a
  FunctionFS/configfs/dummy_hcd USB fixture and a guest USB bulk bridge, then
  proves actual USB AUTH/root/binary readout in the exact pinned kernel with
  FULL original vendor+generic overlay. No physical phone I/O/write/reboot/
  screenshot/CI. LAST physical state still actual0112 boot_b SHA256
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, firmwareFastboot/B/unlocked. Historical, not fresh
  observation. Android userdata and all original backups retained. No actual
  iOS userspace/display/touch/storage-write success added.
- Exact pinned Image config has CONFIG_USB_DUMMY_HCD=y, USB_F_FS=y,
  USB_CONFIGFS_F_FS=y and CONFIGFS_FS=y. Actual previous serial also showed
  dummy_hcd.0 host registration. This supports a REAL in-guest USB path without
  changing kernel/modules. New --usb-ffs-test mounts only configfs + FunctionFS,
  creates only ffs.adb (NO mass-storage or fastboot function), and uses exact
  dummy_udc.0. Never select first UDC on hardware: stock init.recovery.mt6895.rc
  pins physical controller11201000.usb0; dummy is not that controller.
- New usb-fixture.rc sets adbd TCP port-1 and removes listen_addrs. Stock adbd
  writes real FunctionFS descriptors/strings and creates ep1/ep2. An immediate
  init sys.usb.ffs.ready property trigger performs one link/UDC write, guarded
  by bind_attempted0→1; actual UDC readback is separately checked, never inferred
  from attempted property. Probe requires unique18d1:d001/syntheticserial and
  enumerated ff/42/01 interface0 with bulk OUT02/IN81/packet512. QEMU kernel
  reports real USB_STATE=CONFIGURED, FUNCTIONFS_BIND and FUNCTIONFS_ENABLE.
- dummy_usb_proxy.c is a QEMU-only bridge. It rejects non-dummy sysfs ancestry,
  foreign serial/vendor/product/descriptors/char-node identity before USB claim.
  USBDEVFS CONNECTINFO validates devnum; only interface0 is claimed, no detach/
  reset ioctl. It forwards bounded complete ADB frames over actual USB bulk
  ioctls, validates magic/size/checksum, keeps two TCP sessions, and implements
  NO AUTH/shell response itself. Guest TCP port5555 belongs to proxy; original
  adbd TCP disabled. Host adb_wire still connects ONLY127.0.0.1 through restricted
  SLIRP, never host ADB server/USBenumeration or physical USB. Two child/parent
  directions handle actual USB; limits128frames/direction/session,25sidle and
  bounded payload I/O. ZLP handling present but no explicit IN-ZLP observed in
  final test; do not claim that branch tested or full USB compliance.
- Final usb-auth-final4 TERMINAL PASS/QEMUrc0 under exact refusal kernel+full
  vendor prefix. No initial FunctionFS bind timeout. Actual USB OUT CNXN2frames,
  USB IN AUTH3challenges; wrong signature rejected, pinned key accepted. Root
  shell returned syntheticserial/secure1/B/no_data/currentnonce. Actual8192B
  binary readout byteidentical; USB WRTE2048/4096/2048 observed. SHA256
  dc404a613fedaeb54034514bc6505f56b933caa5250299ba7d094377a51caa46.
  RAM receipt completed, ONE authenticated poweroff command sent via USB, guest
  powerdown observed. RootadbdUID0/policy/virtual-onlymounts/fullneutralization
  all passed; original module tree hidden and no .ko loaded in this fixture.
  Evidence research/ace-ramdiag-20261020/usb-auth-final4/{report.json,serial.log,
  usb-authenticated-binary.bin,usb-wire-verification.json}. Private keys0600.
- Final generic LZ4 SHA
  9cb191edfc43fe344d59b3c7eeb875bc8d4cb018702bdab389a7526e6f27062a;
  combined46033045B SHA
  ab0e521b7646ccaae53553b22ee1aab95489d3527a28e9a76557120d7bf9c511;
  serialSHA d3558396dd31712a51ae7437434ab72b3cf9665a2da3be69dd5b353eb5743b13;
  proxyELFSHA aadb660e76072f677628c9afe1cfa47ff6d374e5854a054c44518f8c676c0bdb.
  usb-auth-rebuild4 TERMINAL PASS: preinit/proxy/generic/combined byteidentical
  with the same pinned public key; source hashes identical. Manifest retained.
- Retained earlier evidence: usb-ffs-attempt0 reached descriptors but printf UDC
  write produced repeated ENODEV/no bind. Echo path worked in attempt1; per-byte
  fragmentation was an inference, not syscall-traced fact. Current init write
  avoids that issue. usb-auth-attempt0 failed host -Werror compile indentation;
  fixed without disabling warnings. attempt1 passed USB AUTH; attempt2/final3
  added8192B test and packet logs. Final3 had an initial stock bind timeout then
  eventual successful transfer; this exposed shell-poll latency. Property-driven
  one-attempt binding fixes it in final4, whose runner now REFUSES any initial
  bind timeout. Older passing transport criteria do not prove new sequencing.
- Five actual-parser USB host guards cover exact full/high-speed descriptors,
  all truncated prefixes, identity/config/interface errors, duplicate/bad bulk
  endpoints and500bounded random inputs. All34 RAMdiagnostic tests PASS1.223s.
  Default TCP regression tcp-regression-usb4 PASS/QEMUrc0, serialSHA
  fa12bd2d1ce6c4a505cf35575586e2fcdd4dbcd0ae32c7b04d3dc6e72074e052.
  No physical image or native XNU rebuild generated this turn. All QEMU runs
  and rebuild/download/host test handles are all terminal; no live action remains.
- NEXT concrete work: integrate module bundle with physical-only exact UDC
  controller readiness and source-grounded UFS/provider checks; inspect firmware
  bootloader-return driver dependencies because USB/UFS module closure alone
  does not prove reset-to-Fastboot support. QEMU USB fixture/proxy MUST NOT be
  treated as physical MT6895 USB startup. Then direct-root auto-controller must
  retain native fresh token/pstore/refusal/full boot+vendor hashes/serial and
  one-command firmware return, with physical loader failure/recovery design.
  No userdata write until independent no-data physical diagnostic loop passes.

## ACTIVE HANDOFF: guarded RAM module loader executes in exact-kernel QEMU (2026-10-20)

- Implementation/tests/evidence documentation committed fea03bd; this handoff
  records the exact milestone. Private bundles/modules/keys/logs stay ignored.
- Previous module-plan turn 2c8ee47/b80bccf is PROGRESS. This turn implements
  compile-time pinned module bundle + freestanding loader and real kernel
  insertion/refusal fixtures. No physical phone I/O/write/reboot/screenshot/CI.
  LAST physical state remains actual0112 boot_b SHA256
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, firmwareFastboot/B/unlocked. This is historical, not
  a fresh observation. Android userdata and original backups remain intact.
  No actual iOS userspace/display/touch/storage-write proof added.
- New module_bundle.py re-reads pinned original vendor/kernel, verifies explicit
  plan SHA, plan source hashes and independent hard/pre/post/startup order.
  It checks each exact archived module hash/size, relocatable ELF64 AArch64,
  internal name and release/vermagic metadata; no ABI bypass. Serial identity
  and gate paths are compile-time constants, not commands. Full45 bundle built
  ONLY for synthetic RAMDIAG_QEMU_FIXTURE identity, NOT a phone candidate.
- New module_loader.c guards root/nonPID1/RAM root/tmpfs scratch/no_data,
  exact uname release+architecture, B suffix and exact expected serial from
  bounded cmdline/optional bootconfig. This is release identity, not a runtime
  kernel/partition hash proof; controller still must check full hashes/token.
  Atomic exclusive /tmp/ace-ramdiag-modules.consumed latch before preflight;
  every module must hash correctly before ANY insertion. Bytes are copied into
  memfds, all write/shrink/grow/seal seals added+rechecked; finit_module receives
  the SAME sealed RAM copy, empty arguments, flags0. No force/unload/retry/reboot
  or persistent mount/block operation implemented. Failures exit1 with evidence.
- Sysfs-directory gate is checked before its consumer, with actual SYSFS_MAGIC
  and monotonic15s deadline/poll cap. Full45 bundle gates extcon on registered
  /sys/class/tcpc/type_c_port0. This path is source-derived; ONLY an existing
  generic sysfs directory and a missing TCPC path were tested in QEMU, not
  actual TCPC registration/IRQ/role. Kernel driver probe inside finit_module
  can itself stall; the gate deadline is not an overall hardware watchdog.
- Final module-insert-final2 TERMINAL PASS rc0, exact pinned Android Image.
  Actual stock reset-ti-syscon.ko (no matching QEMU device) inserted from sealed
  RAM copy and observed in /proc/modules. Second invocation rejected consumed
  latch rc-17 before insertion. Same run passed wrong-key rejection/trusted
  root ADB/current command nonce/RAM receipt/ONE authenticated poweroff/QEMUrc0,
  policy/rootUID/virtual-only mounts/no_data. This is module syscall+transport
  component evidence, NOT MT6895 reset hardware or full45 probe evidence.
  Private report research/ace-ramdiag-20261020/module-insert-final2/report.json:
  ramdiskSHA4f2995efb02ea7199a8dd130b4bcd1d07534a52edb4896dba5ecafb2f0290ff6;
  fixtureloaderSHAfbe04584e8dd477e7cdab9c71a684021d6f47d9742a36d84f4d687feeece7a05;
  serialSHAa108b9da76611c2fa92bf42c49b95644090064f4809b206fefb732e8aecc182d.
- Refusal QEMUs all TERMINAL PASS COMPONENT ONLY, each QEMUrc0:
  module-hash-refusal0: second of2 modules corrupted; SHA refusal before first
  insertion, empty /proc/modules, serialSHA
  82e413a0949f0b17e51b17d35e8393853a74cb418087fcf8ab1f1e1b2e3cb2a4.
  module-gate-refusal0: TCPC path absent, deadline-110, no insertion; serialSHA
  b23cfe7fd5bfc574aa5e673770adf708ecdfcdae8229acca008aaa1953c20bc3.
  module-syscall-refusal0: preload reboot-mode; reset inserted then second
  finit_module returned EEXIST-17; loader exits1 with partial modules retained,
  no unload/retry; serialSHA
  11f6b47901b328bf657b9c9b4a8f7d70f3df3a9c68fbe2009b7134a11256f158.
  module-serial-refusal0: wrong expected serial refused before latch/insertion;
  serialSHA88c5558ad3a1392b7bddf4fdfc1adca10825f832edf0d6656d84d2913f44cca1.
  All compiled same module_loader.c SHA
  112d11d80e7cc8f99bd3aa205edfcb9190948e88cf7445860b40358ac9a1ca82,
  with explicit different fixture headers. Negative fixtures are not startup
  success. module-insert-attempt0 failed host gate validation (/sys root not
  accepted); fixed fixture to /sys/devices, preserving restrictive gate syntax.
- Full vendor/auth regression vendor-overlay-loader-regression7 PASS, serialSHA
  7f0a5525341352f74728e86eba42305602cee50fde6ea42d414e4f21f69486dc.
  Runtime full-overlay mode still hides ALL original modules and loads none;
  QEMU fixture intentionally uses filtered RAM image, never full45 MTK probes.
- Full45 module-bundle-final1 and module-bundle-rebuild1: all47 output files
  (45original modules + header + loader) byteidentical. Full loader SHA
  5cf8ca0c725e5ccc87deb9ad70700ed86505847dc026a77e77067b73f959ed74;
  headerSHA3218c3f96d1e24957919ad4f5cbd69fb3eb8e9ff23fe1226aa067bc389cea9ea.
  Latest rebuild reportSHA
  3d991da3662455df509413c110907db1f88d1338fde97457fa40f192a9fbd727,
  reproducibility.json retained. Full45 were COMPILED/BUNDLED, NEVER executed.
  New SHA header checked against hashlib for padding/chunk boundaries, binary
  streams and million-byte vector. All29 RAMdiagnostic host tests PASS0.702s.
  All host/QEMU handles terminal. No unrelated fullsuite or CI/kernel rebuild.
- NEXT: implement remaining actual provider/binding/UDC/UFS readiness checks,
  bootconfig serial parser coverage and physical loader failure/recovery design.
  Then integrate module bundle into controlled full vendor overlay profile,
  direct-root automatic controller with native current token/pstore/refusal
  record/full boot+vendor hashes/serial and one-command firmware return.
  Do not execute full45 as an unreviewed bare insmod list or call insertion
  completion a hardware-ready marker. No phone image generated this turn.
  Firmware precedence/USB/UFS physical RAM diagnostics remain unproven; no
  userdata write until the independent no-data physical diagnostic loop works.

## ACTIVE HANDOFF: exact module/provider proposal and TCPC startup requirement (2026-10-20)

- Code/tests/evidence documentation committed 2c8ee47; this handoff records the
  exact milestone. Private source/module bytes/reports remain ignored.
- Previous full-overlay turn ba4f60d/1abb481 is PROGRESS. This turn adds a
  pinned, offline module/provider planner and establishes an additional concrete
  USB startup requirement from official source. No physical phone I/O/write/
  reboot/screenshot or CI. LAST physical state remains actual0112 boot_b SHA256
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, firmwareFastboot/B/unlocked. No fresh device observation;
  no ADB screenshot possible without a verified ADB connection. Android userdata
  and protected backups remain intact. iOS usability is NOT achieved.
- diagnostics/ace-ramdiag/module_plan.py reads original hash-pinned vendor CPIO
  directly (not a possibly modified extraction), all270 .ko members, exact dep/
  alias/softdep metadata, exact live FDT68c811...8560b and pinned refusal kernel
  8d555b...f11d0. Normalized module-name ambiguity, unknown refs, unsafe paths,
  incomplete dep coverage, duplicate metadata, graph cycles and malformed DT
  specifiers refused. Hard/pre/post dependencies get deterministic topological
  ordering; DT edges remain separate from insertion order and probe completion.
- Final private module-plan-final2/report.json SHA256
  b2850e95aebfb2fa2dddfad6a6565729d5db77e6c593011319a15b318cb697c6:
  66nodes/170provider edges/45modules/4311600 original module bytes. All hard/
  pre/post ordering constraints independently checked. All46 scpsys clock
  provider+argument tuples exactly match prior independent source/DT closure.
  No reached node disabled. Remaining unmapped compatibles are root MT6895,
  /clocks/clk26m fixed-clock, /interrupt-controller arm,gic-v3, /soc simple-bus;
  not silently treated as proven built-in. No remaining unparsed properties
  FROM THE EXPLICIT binding list; unknown binding formats/generated children
  still require source review. This is an OFFLINE PROPOSAL, not a loader or
  physical startup proof. No modules executed this turn.
- provider_overrides.json has16 source-observed mapping records with exact
  URL/commit/sourcehash checked against local source bytes and table strings.
  Missing aliases covered for clock/scpsys/UFS/pinctrl/typec mux drivers. MFD
  mt6363/mt6368 regulator children require BOTH source cell name and exact stock
  platform alias. This is not instruction-equivalence proof of stock modules.
- startup_preconditions.json records source-observed extcon failure behavior:
  extcon-mtk-usb.c320-334 gets TCPC by tcpc string, returns ENODEV when absent;
  probe566-577 merely logs failure then returns0. Therefore later TCPC arrival
  is NOT assured to retry notifier setup. Pure symbol order had extcon first.
  New explicit constraint TCPC module before extcon gives indices41<42, but
  insertion alone is NOT the gate. Loader must wait current registered
  /sys/class/tcpc/type_c_port0 before extcon probe. tcpc_mt6375.c2758 reads
  tcpc,name,2666 passes descriptor; tcpci_core.c431-448/895 creates named device
  in class tcpc. Supporting source hashes are retained/pinned in that file.
  Named DT lookup is unique; missing/ambiguous names rejected by planner.
- Re-extracted IKCONFIG from exact pinned Image with bounded zlib and IKCFG_ED
  check. 232546B SHA256
  7d939635d77acbaa49a3e4ab2bdbb154c0a2c5e393b8057fa11a49071b56f149,
  byteidentical to older ace-offline/stock-kernel.config. This is config evidence,
  not proof every selected module ABI/probe is compatible. New module-plan-
  rebuild2 report.json and kernel.config byteidentical to final2; source/input
  hashes and snapshots retained. All23 RAMdiagnostic unit guards PASS0.859s;
  pycompile and diffcheck PASS. No new QEMU execution: existing init/auth binary
  and runner unchanged. All host download/planner handles terminal.
- Official source additions under ignored provider-source/manifest.json include
  seven clock-driver sources, pinctrl, correct composite SPMI core/debug source,
  extcon, typec mux, TCPC driver/class core and Makefiles. Exact revision remains
  OnePlusOSS8baa5a377e2776402de745579cc3835d08ee1cca. Preserve failed path404s.
  Correct SPMI Makefile links spmi-mtk-pmif-core.o + spmi-mtk-debug.o; initial
  spmi-mtk-pmif.c path404 did not mean source unavailable. Direct gh api read
  had no configured authentication; public GitHub API was rate limited403;
  pinned raw source fetches succeeded. No CI dispatch attempted.
- NEXT concrete work: bundle selected exact module bytes at a new controlled
  RAM path (original /lib/modules stays hidden), implement bounded one-pass
  module startup and actual provider/TCPC readiness checks, test loader failure
  handling against exact kernel. Do NOT execute the proposal as a bare insmod
  list. Module insertion can probe other enabled instances outside this DT
  closure; deferred probes and source-specific nonfatal errors need evidence.
  Then direct-root automatic controller must preserve native fresh token,
  pstore/refusal record/full boot+vendor hashes/serial and one-command firmware
  return. Physical firmware unpack precedence and USB/UFS startup remain open.
  No userdata write until independent no-data physical diagnostic loop works.

## ACTIVE HANDOFF: full vendor + generic RAM overlay authenticated in QEMU (2026-10-20)

- Code/tests/evidence docs committed 1abb481. This handoff records that commit;
  private artifacts/keys/logs remain ignored. Diff check and pycompile PASS.
- PROGRESS; usable iOS remains unachieved. Full original vendor ramdisk plus
  controlled generic overlay now passes QEMU init/adbd/authenticated root RAM
  commands. No phone I/O, flash, reboot, new screenshot or CI this milestone.
  LAST physical state remains actual0112 boot_b SHA256
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, verified firmwareFastboot/B/unlocked; Android userdata
  and all original backups retained. This is historical, not a fresh device check.
- New --vendor-overlay-test retains the exact original compressed vendor prefix
  (928 nontrailer CPIO members), appends same-format legacy LZ4 generic ramdisk
  without padding. Original vendor compressed SHA256
  0efe5c4c5da3f4a3bfdedd40c25755bb7e16544b272a38d231d5fe9adafba098.
  This tests kernel unpack order, NOT physical LK/firmware precedence.
- All11 original .rc/.prop/fstab startup paths except controlled init.rc are
  comment-only overlays and checked in the guest. Original recovery binary is
  replaced by empty nonexecutable marker. /lib/modules hidden by noexec/nodev
  tmpfs; /proc/modules empty. Host verifies original RAM data tree contains ONLY
  empty data/vendor + data directories; preinit removes ONLY those empty dirs
  after PID1/RAM/B checks, refusing nonempty directories, never deleting content.
- New no-libc B-slot parser checks bounded64KiB cmdline and optional bootconfig
  BEFORE stock init/policy. Missing/wrong/malformed/conflicting suffix refused;
  every recognized value must B. Four host parser tests pass incl duplicate
  conflicts/cross-authority and bare malformed bootconfig key. Original policy,
  init/adbd/kernel pins remain unchanged; stock first_stage/selinux_setup avoided.
- Actual vendor-overlay-final6 TERMINAL PASS rc0. Full overlay runtime checks,
  policy, root shell/adbdUID0, virtual-only mountinfo/no_data all PASS. WrongRSA
  signature refused, pinned key accepted; fresh shell nonce + /tmp receipt then
  ONE authenticated poweroff command, observed guest powerdown. Private report:
  research/ace-ramdiag-20261020/vendor-overlay-final6/report.json.
  Generic LZ4 7568761B SHA256
  2ca92cfdfdcf5557f93c9cc65835573cb0a5c7ecee6274526978992ca2ad87c3;
  combined46025601B SHA256
  795e3bb4b08ac876767349f3c69a419bbb4b7f385563629fed328289d51f4d6d;
  serialSHA256041c634f2837e5f7791c4634ad7b3372d85719ee9644d71af3253ac68eba41e1.
  vendor-overlay-rebuild6 preinit/generic/combined byteidentical, source hashes
  match, same pinned public key. Keys remain ignored/private0600.
- Final conflict VM vendor-overlay-conflict-final6 PASS preinit refusal ONLY,
  no stock init, serialSHA16e047a98fd6bfd91196ad10323e214c99a81e13d465f347ccfde0a98db2a481.
  Earlier wrongslot/noslot VMs also refused before stock init. Default no-network
  stage2-regression-final9 PASS rc0, serialSHA
  e26f824f30d0ffe638918269ce68e000de7e70dc8e8ef42a716576af1ca31616.
  All12 adb/slot offline tests PASS0.834s. All QEMU/build handles terminal.
- Failed overlay attempts0..4 retained. 0 original empty RAM /data directories;
  1 parent-only rmdir correctly refused ENOTEMPTY; 2 missing adbd log visibility;
  3 kmsg_debug revealed SIGABRT random_device urandom Permission denied;
  4 standard null/random/urandom permissions fixed startup, but original
  system/build.prop made adbdUID2000 and trusted key unreadable. Neutralizing
  original .prop fixes that; attempt5 passed, final6 adds final parser hardening.
  Adbd now oneshot with stdio_to_kmsg and ADB_TRACE for bounded retained evidence.
  Cpuset warning was not the established cause; do not promote that earlier guess.
- NEXT: implement physical RAM diagnostic module/provider startup from the exact
  live FDT and pinned module dependencies; preserve native fresh-token/pstore
  record, full boot/vendor hashes and serial identity. Add explicit direct-root
  controller profile/one-command firmware return before any physical candidate.
  Firmware unpack precedence, MT6895 USB/UFS modules and no-userdata physical
  readout loop are STILL UNPROVEN. No userdata write until that loop passes.
  Preinit failure poweroff is QEMU-only, not a physical recovery design.
  No iOS root mount/userspace/display/touch/persistent operation proof added.

## ACTIVE HANDOFF: authenticated root ADB without /data PROVED IN QEMU (2026-10-20)

- Implementation/tests/evidence-docs milestone committed c1554d0; this follow-up
  records the exact commit. Private keys, source downloads and logs stayignored.
- Previous turn e40e84d/3fa5a40 is PROGRESS. This turn implements optional
  --tcp-auth-test + bounded loopback-only adb_wire.py +8offline guardtests.
  No hostADBserver/USBenumeration/phoneI/O. Exactstock Android Image/vendor
  pins unchanged. All new host/QEMU/download handles TERMINAL; no REA open.
- Actual tcp-auth-attempt6 TERMINAL PASS rc0. WrongRSA signature→freshAUTH
  challenge; pinnedRAM /adb_keys signature→recoveryCNXN. Authenticatedshell
  returnedroot/syntheticserial/secure1/B/NO_DATA/currentrandomcommandnonce.
  Secondstream wrote+readexactnonce in/tmp. After COMPLETEreceipt hostsent
  ONCE authenticatedshell reboot-p; actualguestpoweroff/QEMUrc0. Monolithic
  policyloaded, shell+adbdUID0, no/data, virtual-onlymountinfo alsoPASS.
  This proves QEMUAUTH+RAMdiagnosticcommands, NOTAceUSB/firmwareFastboot/iOS.
- Private research/ace-ramdiag-20261020/tcp-auth-attempt6/report.json;
  ramdiskSHAdd30a23799d91f8bbe40be264821b5e2fcd82deef35deff6d56ce0bd3ec9d9a7;
  serialSHAe71d0fa84ff3bdc34bd07ad66ca98a6a6e2b4a2e1733e50353966ecbeda5b9ee.
  Ephemeraltrusted/untrusted keys stayprivate0600, testdir0700; onlypublickey
  hashpin entersramdisk/rootreadableadb_keys. Wire neveroffersnewkeyforUIauth.
  tcp-auth-rebuild6 preinit+ENTIREramdisk byteidentical withsamepublickey;
  default stage2-regression8 PASS/rc0/serial
  f20abfc987c72b8c855aef1fe4720a2191d57b9fc1ac7299e8b69bbd1fb8ac8f.
  Final8unitguardsPASS0.934s; pycompile/diffcheckPASS. No unrelatedCI/fullsuite.
- Every failed authattempt0..5 retained:0virtioNICabsent;1clientversiontoo
  strict (actualCNXN01000001, legacychecksumstillverified);2printfmissing;
  3localguestpoweroffracedreceipt;4reusedlocalstreamID/lateclose;
  5clientrejectedknownoldCLSE. CurrentfreshIDs+closeACK+max4exactknownclosed
  CLSE skips, foreignstream/malformed/oversize/checksum/timeout/unknownrole
  stillrefused. Completednonce receipt precedes onepoweroff; guestwatchdog
  printsFAIL, neverturns a failedhandshake/return intoPASS. No phone retries.
- QEMUtransportusesbuilt-in PCIxHCI+CDC USBnetwork fixture (eth0), restricted
  SLIRP and127.0.0.1forward only. KernelconfighasnoVIRTIO_NET/MMIO; no kernel
  changes/modules needed. This is NOTphysicalMTKUSBhardwareevidence.
- Independentprovider review: fetched five more officialsourcefiles at
  OnePlusOSS8baa5a377e2776402de745579cc3835d08ee1cca into provider-source;
  URL/hash manifestretained inclSPMIhostpath404. Sourceclockregistration maps
  clk-mt6895 TOP/VLP, peri PERICFG/IIC/UFS_AO/UFS_PDN, bus INFRACFG. These
  sourcefacts doNOTproveexactmoduleinstructionequivalence oractualprobe.
- Genericmtk-scpsys.c1258–1311 getsregulators+clocksforALL40domains first;
  onlyoptionalsupplyENODEVignored, othererrors/defer abortentireprovider.
  IndependentlyreproducedexactliveDT/sourceclosure scpsys-clock-closure.json:
  ALL46clocknamesrequested (17basicrequests/15unique+31prefixmatchednames).
  BYPASS/DISABLEflags occurLATER; UFSdomain2alone cannotavoid globalcamera/
  displayCLOCKprovider +MT6319supplydependency. Functionalpanel/cameradrivers
  nottherebyrequired. Power-onWARN/PMICIRQlogs needruntimechecks, notjustprobe
  done. mtk_clk_simple_probe+PMICregulatorchildsourcegap nowresolved.
- NEXT: fulloriginalvendor +newgeneric ramdisk overlay QEMU run withoriginal
  RC/fstab/OEMstartup neutralized, moduleautoload controlled, positiveB-slot
  gate BEFOREstockinit. Bind actualfreshnativeFDTtoken/pstore/readoutprofile,
  root/serial/B/fullboot+vendorhash checks andexistingguardedreturn semantics.
  Expand complete clock/supply/moduleclosure fromnewsourcefacts, solveSPMIhost
  source/actualmodule checks. Thenpreparefresh-token physicalboot_b candidate
  usingrealtrustedhostpubkey; one-timewriter+automaticreadoutonlyafterallgates.
  Physicallyprove no-/data USB/logs/Fastboot loop BEFOREuserdata iOSrootwrite.
- Actualphone LASTverified0112boot_b64MiB remains recorded SHA
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, firmwareFastboot/B/unlocked. NOphonewrite/reboot/CI/
  verifiedADB thisturn; noscreenshotavailable. Androiduserdata/originalbackups/
  protected/GPT untouched, nooriginalrestore. FulliOSgoalACTIVE/unachieved;
  rootdriver/display/touch/basicoperations stillunfinished, NOTblocked.

## ACTIVE HANDOFF: no-data init/adbd component RUNS in diskless QEMU (2026-10-20)

- Implementation/probe/docs milestone commit e40e84d; this follow-up records it.
- Previous turn6267004/91ba887 classified PROGRESS. This turn implemented and
  actually ran diagnostics/ace-ramdiag/{preinit.c,init.rc,probe.sh,qemu_stage2.py}.
  This is a QEMU COMPONENT probe, no phone partition image/controller profile.
  All host/QEMU sessions terminal, all REA sessions closed with snapshots.
- Final7 QEMU TERMINAL PASS rc0: real exact stock kernel8d555b...11d0,
  exact vendorbackup bb5a09...9670; bootstrap PID1/RAMroot, directly loaded
  original monolithic SELinux policy, permissive diagnostic guest, executed
  exact recoveryinit second_stage, started stockueventd+shell+adbd. Shelluid0,
  adbd fourUIDs0, ro.adb.secure=1, synthetic QEMUserial, readypropertyset/readback,
  no /data directory, PID1 mountinfo onlyvirtualfilesystems, orderlypoweroff.
  This proves COMPONENT EXECUTION only, NOT authenticated ADB/USB or iOS.
- Final7 private research/ace-ramdiag-20261020/stage2-final7/report.json;
  ramdisk6452678B SHA77b69c6a849e6f6306dd8ccc8f0c0eb1b94288d3c19930498e612fc98d61c7a0;
  serialSHA81efa4bfc125cd350a4d34c9be5d84c21a9214cadd624edd4a1cd3eadc2e1114.
  Independent hostrebuild stage2-rebuild7 preinit+ENTIREramdisk byteidentical.
  Exactsource snapshots/memberhashes/compilecommand retained per finalrun.
- Failed attempts preserved:0 crosslibc headers absent (no target execution),
  1 ELFpureBSS segment beyondEOF gave initEFAULT/panic (QEMUrc0 stillFAIL),
  2/3 reachedsecondstage but55s hosttimeout;4 observer deliberateFAIL/rc0poweroff.
  Corrected initial inference: lastUSBlog was NOT a propertycall hang. Observer
  syscall22/epoll_pwait +wchan/stack proved eventwait. Minimalrc omittedueventd,
  so coldboot gate nevercompleted; add exactstockueventd inearly-init fixedit.
  Attempts5+6PASS; randomtemporaryGCCobjectnames affectedonlylocalELFsymbols,
  --strip-all removes that sourceofhashvariation, final7PASS+exactrebuild.
- New REA recovery-init-property.rea.json saved/closed. IsRecoveryMode only
  access(/system/bin/recovery); QEMUusesemptyNONEXECmarker/norecoveryservice.
  Slot_b fixture forcesroot/prop.default; no-suffix OEMrecoverydefaults canfork
  ueventd and attemptcache/system mounts. DO NOT invoke unsafe defaults branch.
  Stockfirst_stage/selinux_setup nevercalledbybootstrap. Scriptprofile lacks
  trustedhostkey, network, modules, blocknodes, nativeFDTtoken/pstorecollect and
  guardedreturn. Failurepowersoffguest; NOT a physicalrecoverydesign yet.
- Module/DT review in docs/ACE-RAM-DIAGNOSTICS.md: recoverylist notbareinsmod
  order; 18-module symbolclosure onlyseedlowerbound. ExactliveDT addsreset-
  ti-syscon, regulators/clock/powerproviders, USB extcon→chargerOTG/MFD/I2C/
  pinctrl dependencies. Do NOT blanketexcludecharger. LiveUFSnode NOphys/
  phy-names/iommus/pinctrl and no separateUFSphy node; genericrecoveryPHYentry
  notproofrequired. Clock/scpsys missingaliases requiremodule/source evidence.
- NEXT concrete: trustedRAMhostkey+actual authenticatedADB handshake (first
  controlledQEMUtransport iffeasible), pstore/nativecurrenttoken/RAMreadout
  profile withallidentity/B/fullpartitionhash/guardedreturn gates retained.
  Resolve moduleprovider registration+DTprobe checks. Prepare physicalgeneric
  overlay that neutralizes all originalRC/fstab/OEMstartup actions, assert
  slot_b beforestockinit; QEMUprobefilteredramdisk doesNOTprovethephysical
  vendor/genericoverlay. Onlythenfresh-token guardedboot_b one-timetrial.
  Physicallyproveindependentnodatadiagnosticloop BEFOREuserdataoverwrite.
- NOphoneI/O/write/reboot/CI thisturn. Actual0112boot_b remains
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, lastphysicalfirmwareFastboot/B/unlocked. No verifiedADB
  thisturn/no screenshotavailable. Androiduserdata/backups/protected/GPT intact,
  nooriginalrestore. FullgoalACTIVE; rootdriver/iOS/display/touch/usability
  stillUNPROVEN, notblocked. Validation:newstrictQEMU+exactrebuild/compileWerror/
  pycompile/diffcheckPASS; no unrelatedkernelCI or broadtest rerun needed.

## ACTIVE HANDOFF: boot_b-only RAM diagnostic prerequisites (2026-10-20)

- Implementation/docs milestone committed as 6267004; this follow-up records
  the exact commit. Private extracted binaries/snapshots remain ignored.
- OFFLINE milestone only, no phone I/O/write/reboot/CI this turn. Actual boot_b
  remains physical0112 aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746, last verified firmwareFastboot/B/unlocked. No new ADB
  connection/screenshot or new physical boot result. Androiduserdata intact;
  original backups/protected partitions/GPT unchanged. No routine restore.
- Added keyword-only diagnostic_ramdisk + mandatory SHA256 pin to stock-chain
  package helper. Default output retains original ramdisk; replacement only
  permits kernel_size/ramdisk_size header changes, reparses payloads/footer,
  checks both exact payloads, AVB relocation/partition bounds. No new CLI or
  validated RAM profile yet. Actual0112 rebuild byteidentical64MiB; explicit
  original-ramdisk route also byteidentical. Private packaging-compatibility.json.
- Full286tests PASS102.887s; afterward strengthened the alignment fixture so
  BOTH compressed kernel and ramdisk cross pages; relevant8tests PASS5.890s.
  Initial fixture was too small and correctly hit overflow; fixed fixture size,
  no production-guard relaxation. gitdiffcheck PASS. No kernel patch/CI needed.
- Exact stockboot/vendor backups rehashed+CPIO parsed privately under
  research/ace-ramdiag-20261020: boot24entries/vendor929entries/270modules.
  Original recovery rc fscks userdata/cache and mounts persist RW: DO NOT reuse.
  ELF recursive DT_NEEDED closure init/adbd/sh/toybox/linker42files/no missing;
  runtime namespace/dlopen behavior NOT established.
- REA adbd/authlib/recoveryinit snapshots saved and ALL sessions CLOSED.
  Exactauthlib code+16B table establishes /adb_keys then /data/misc/adb/adb_keys;
  trusted ramdisk host key is a design possibility, NOT a physical connection.
  Init main explicitsecond_stage beforefirststage; secondstage properties/
  SELinux labels/ro.boot.init_rc observed. Stock selinux_setup firstcalls
  MountMissingSystemPartitions: do not invoke blindly to bypass mounts.
  docs/ACE-RAM-DIAGNOSTICS.md records hashes/EvidenceIDs/limits/acceptancecontract.
- NEXT: implement controlled PID1/preinit/SELinux setup + minimal rc/properties
  and pinned trusted key; inspect MountMissingSystemPartitions conditions if
  reusing any stock setup. Establish generic/vendor overlay precedence and
  USB/UFS module dependency loading without OEM update/recovery actions.
  Build actual diagnostic ramdisk, QEMU-test THAT environment (old refusal QEMU
  swaps in fixture PID1), add explicit no-su/no-boot_completed/RAM controller
  profile retaining all identity/token/B/hash/guardedreturn rules. Only then
  fresh-token guardedboot_b automatic trial. Physically prove no persistent
  userdata mounts + logs/automaticFastboot BEFORE userdata root overwrite.
  Rootdriver/iOS/display/touch/basicoperations still unfinished; goalACTIVE.

## LATEST ACTUAL0112: genuine LUN2 capacity/blocks/GPT verified against Android (2026-10-20)

- Writer55527/controller72976/offlineinspection/independentAEE33381 all
  TERMINAL SUCCESS. Retained actualboot_b64MiB SHA
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746. V5diagnosticADB76.1s/root/B/boot+vendor/currenttoken
  verified; automatic_loop_verified=true; refreshedidentity/token return one
  rc0 command, physicalfirmwareFastboot product/B/unlocked/is-userspace=no.
- NEW PHYSICAL: actualF0 resetUA recognized once; secondTUR GOOD. READCAP16
  OCS0/response0/status0/residual0: lastLBA03b95fff, block4096, capacity
  255919652864B. READ10 blocks0/1 OCS0/type21/response0/status0/residual0;
  CRC32f59d9d0e/79b497ad. GPT92B stored/calculatedCRCfedaebac.
  Offline independent same-trial Androidsdc capacity/block0+1CRC/GPTmatch PASS.
  Genuine bounded diskread now PROVED, not just NOP/hoststatus. No media
  published, writes performed, rootmounted or usableiOS. OtherLBAs untested.
- Pmsg17695B SHA8c1ad39c6a93cb4b190a4b2a8e5f462e406f8da6fd6ab2c818bd2aea76c0a3dd.
  AEEattempt0 complete16189952B SHA
  cf3a3c5afdc87478aadd1a4a87b9a13f63d4e0d115341ad2646cf2d9118500fc;
  V5identitylookup0verified, no outage observed thistrial. Independent archive
  a55e3e94344a00aa4421276f08d93deb0032a6929e6129f32a3ae606a961984c,
  55entriesCRC+size and rawringbyteidentical. Inspected21:33 Androidhome
  screenshot (noUSBdialog), NOTXNU/iOSdisplay. All private under sensevalid.
- Source1128f89ecc/host9bd3ea6/remotea24fad1; CI39429611804/job118650915354
  success186s/cached1071hits1miss/artifact12266979103/hash above. Final284tests/
  sixcompiles/exactheader/source/actualoutlinedmask/SMC/native9+Centry+4Android
  allPASS. docs/ACE-UFS-RELATED-FIXES.zh-CN.md updated with latest proof scope.
- NEXT concrete prerequisite beforeuserdataoverwrite: inspect exactstock boot
  andvendor ramdisk/init/adbd dependencies OFFLINE; design boot_b-only diagnostic
  ramdisk using existing pinned Android refusal kernel, currenttoken/pstore and
  trustedADBidentity, RAM-backed scratch/no persistentuserdata mounts. Physically
  verify no-/data diagnosticUSB/readout/hash/currenttoken/automaticFastboot path
  FIRST. Existing vendor_bootdiag prototype is OFFLINE only/protectedpartition
  not authorized forwrite; do not use it as excuse to flash vendor_boot.
- Rootdriver next: persist the proven MTK controller/DMA owner (currentProbe is
  stacklocal), serialize requests, validate GPT/partitionbounds for Aceuserdata
  LUN2 and expose bounded BSDroot path. Do not copy SweetQualcomm/LUN0/reset/
  cache assumptions, reinitialize proven host blindly, or write unrelatedLBAs.
  Existing HFSrootimage/Sweetuserspace work requires Aceintegration+realmount/
  launchd/display/touch/persistentbasicoperations tests. Androiduserdata still
  intact. Preserveexperimental112/backups/protected/GPT. Allprocessesterminal,
  allREAclosed. Fulloriginalgoal ACTIVE/unachieved, NOTblocked.

## CURRENT0112 written; automatic V5 trial starting ONCE (2026-10-20)

- Writer55527 TERMINAL SUCCESS:onlyboot_b64MiB SHA
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746; send1.419s/write0.144s/total1.566s.
  Finalidentity/B/unlocked/firmwareFastboot/geometry/source/hash/backups PASS.
- V5controller startingONCE withrefs/screenshots/AEEintegrity+boundedidentity
  lookups. ActualUA/TUR/capacity/blockresultUNKNOWN. Neverrestartwriter/
  controller. Nooriginalrestore/protected/GPT/userdata/slotwrites. Goalunfinished.

## CURRENT0112 packaged; guarded one-time boot_b write starting (2026-10-20)

- Native15683 TERMINAL SUCCESS9native/Centry/4Android/package284tests.
  Fresh64MiB candidate SHA
  aab18c81796ed6551d4914901c590ce36d61cd203fa0975bef3363cee35124d4,
  token2ffa2f269c2f3746. ACTUAL1110bdd...cccb explicitseparatereturn receipt
  bound;newtoken absentpriorpmsg/latch+refusalguards verified;19backups rehashed.
- Starting guardedwriter onlyboot_b after finalserial/product/B/unlocked/
  firmwareFastboot/geometry/source/hash/backups gates. This line PRECEDESwrite;
  consult sensevalid/phone-trial/state.json andflashlog forexactoutcome.
  No112physicalUA/TUR/capacity/blockyet. Neverrestartwriter/controller; nextv5
  boundedAEEidentitywait controller ONCE. No rollback/protected/GPT/userdata.

## CURRENT0112 CI accepted; actual linked sense mask verified; native LIVE (2026-10-20)

- CI39429611804/job118650915354 TERMINAL SUCCESS cachedBuild186s,
  1069direct+2preprocessedhits/1miss. Artifact12266979103 ZIP SHA
  432cd72d28cf92d2faccc45649a79ee4b0ccac17c9b15640ffce67718a6b3304;
  exactcommit/ACE/cachedprovenance/SHA256SUMS/readinessstrings/entry/cacheCIVAC
  verified. Kernel17557960B SHA
  3846d1c7d547a256c2ad4cc77f12072475d8c7296fa9dac2e36dc74bdae8d366.
- ActualLINKEDfixedSMC ONEsmc/exactABI PASS. Initial extra static mask check
  searchedcommand(), but compiler outlined the headerhelper; assertion was
  wrong inspection target, not kernel failure. Native15683 already started
  host-only through shellfallthrough; NOTrestarted. Correct outlinedhelper
  disassembly verifies ldrb[r+34] /AND7f/CMP70 and commandcall. Saved proof.
- Freshnative15683 LIVE9cases/Centry/4Android/package284tests. No112phonewrite
  yet;actual1110bdd...cccb retained. Do notrestart. Fullgoalunfinished.

## CURRENT0112 cached CI dispatched ONCE (2026-10-20)

- Local112complete8f89ecc (host/V5/header/tests9bd3ea6); remote
  a24fad106133e8a818d94186dcd6ba59093edfcf. ExactUIbranch/commitverified,
  ACE13.5DEVELOPMENT cached/diagnosticfalse; run39429611804/job118650915354 LIVE.
  Do notredispatch. Final284tests52.911s/sixcompiles/fullpatchheader/SMC/ABI/
  SWEETunchanged/19backups/identityFastboot PASS. No112phonewriteyet.
- Actual1110bdd...cccb retained, physicalfirmwareFastboot after separate guarded
  evidence-onlyreturn; originalcontrollerfailure retained. Nextpipeline binds
  that explicit separate-return receipt, freshnative/token, v5AEEidentity waits.
  FulliOSgoalACTIVE/unachieved; no rollback/protected/GPT/userdata writes.

## ACTIVE HANDOFF: 0112 sense VALIDbit and V5AEE identity waits validated (2026-10-20)

- Source112 onlycorrects fixedsense responsecode low7bits; F0/70 accepted,
  every otherheader/sense/key06/ASC29/ASCQ00/length/OCS/hardware/one-UA gate
  retained. Actual-method test now uses syntheticF0+informationfield; no private
  device dump added to git. V5collector bounded identity waits preserve all
  observations, max3archive reads/no extra rebootretry; transient+absent tests.
- Final284tests PASS52.911s; sixACE/SWEETcompiles/SWEETunchanged/importsABI/
  fullpatchsource+header/singleSMC PASS;19backups/expectedidentityfirmwareFastboot
  reverified. Host/header/V5/test changes committed in9bd3ea6 along with111
  milestone; thiscommit completes kernelpatch112 and handoff. No112phonewrite.
- Pipeline research/ace-ufs-sensevalid-20261020 binds ACTUAL1110bdd...cccb and
  explicit separate_return_verified after originalcontrollerfailure. Newtrial
  mustuse fresh token/currentv5 and cachedCI. Do not use110 as previousreceipt
  or restart111writer/controller. FulliOSgoalACTIVE/unachieved.

## LATEST ACTUAL0111: separate guarded return complete; sense VALIDbit established (2026-10-20)

- Originalcontroller72214 FAILED at transient AEE identity lookup after partial
  read; neverrestarted. Evidence-only continuation61881 TERMINAL SUCCESS:
  currentrecord/root/B/boot+vendor reverified, attempt1 complete15983104B SHA
  172de89cdd6fb594e600fd4bf78f90f863abdffca75cfbbd4b63e320054d9ac9;
  remainingreadcount<=3, references/screen, refreshedtoken/identity/returnrecord/
  existingexactrebootpolicy and physicalfirmwareFastboot verified. State keeps
  original_controller_failed, automatic_loop_verified=false,
  separate_return_verified=true. No normalboot/XNUrepeat/flash/restore.
- Actual111boot_b0bddabba466a2a61b84661962af7e7fb8ed75006dea419cf22850eb73a90cccb,
  token62f67e99a7c8decd retained. Rawresponse senseF0 explains strict111exact70
  refusal; fixedcode low7bits70, VALID informationbit7 set. No TUR GOOD/data yet.
  Pmsg16966B SHAa5525b2cf474aa45a8beef9f34313cc958ad1ae7ef4ce3718bece27bb968d6db.
- Independent AEE first93786 wrote evidence but exit143; OFFLINE recheck23998
  TERMINAL SUCCESS55entries CRC+size and byteidenticalpmsg. Archive SHA
  6b6f9ef7c767d2dcca00a3ab9601dce6730fb02917678359a0f7198c24468b01.
  Both screenshot21:09/continuation21:13 inspected Androidhome+USBpicker only.
- Next112 masks responsecode&7f as upstreamscsi_normalize_sense, accepts actual
  F0/70 currentfixedsense with allothergates unchanged. V5AEEcollector waits at
  most5identitylookups/2s before each read, retains lookup+partialobservations,
  keeps total3archive reads and existingno-device-only rebootretry protocol.
  Missingidentity exhausted is an explicit AEE limitation; no unverified read.
  Tests cover transient/persistent absence; neverrestartconsumedcontroller.
  Current112source/hosttests in progress; no112CI/image/phonewrite. Fullgoalunfinished.

## CURRENT0111 original controller STOPPED; evidence-only continuation starting (2026-10-20)

- Controller72214 TERMINAL FAILURE after ADB76.1s, root/B/boot+vendor and
  current-token validated, screenshot/pstore/dmesg saved. AEEattempt0 truncated
  12288000B SHA20f542849b514a5e2c2cc8ae02696dac38358329219c7747c26bfdced6aa4e16;
  immediate identity lookup empty -> stopped BEFORE bootloader-return command.
  Do not restart controller/writer/normal boot. Actual1110bdd...cccb retained.
- Fresh observation expected serial-bound USB+TLS ADB are back; noFastboot.
  Prepared private finish-evidence-after-controller-stop.py ONLYremaining
  AEEreads(attempt1/2), currenttoken+root/B/hashes, boundedreference8KiB reads,
  separate screenshot, then existing refreshedidentity/token/return-record/
  exactrebooterrorpolicy and firmwareFastboot checks. No flash/normal boot/
  XNUretry. Preserveoriginalcontrollerfailure; separate_return_verified records
  this recovery, not falsely claiming original automatic controller completed.
- Newactual pstore16966B SHA
  a5525b2cf474aa45a8beef9f34313cc958ad1ae7ef4ce3718bece27bb968d6db:
  samevalidinitthenTUR06/29/00 rejected. Rawprefix reveals sense codeF0
  (fixed70 with information VALIDbit7), while111requiredexact70. Strictrefusal
  is explained; nocapacity/block result. NEXT112 recognize standard VALIDbit
  without changing other gates; source-backed exact observed discrepancy.
  Mustfinishcurrentevidence/return before newtrial. Fullgoalunfinished.

## CURRENT0111 written; automatic trial starting ONCE (2026-10-20)

- Writer43316 TERMINAL SUCCESS:onlyboot_b64MiB SHA
  0bddabba466a2a61b84661962af7e7fb8ed75006dea419cf22850eb73a90cccb,
  token62f67e99a7c8decd; send1.386s/write0.141s/total1.529s.
  Finalidentity/B/unlocked/firmwareFastboot/geometry/source/hash/backups PASS.
- Automatic v4controller startingONCE withrefs/screen/AEEintegrity. ActualUA/
  TUR/capacity/block resultUNKNOWN. Neverrestartwriter/controller; nooriginal
  restore/protected/GPT/userdata/slotwrites. Fullgoalunfinished.

## CURRENT0111 packaged; guarded one-time boot_b write starting (2026-10-20)

- Native98662 TERMINAL SUCCESS9native/Centry/4Android/package283tests.
  Fresh64MiB candidate SHA
  0bddabba466a2a61b84661962af7e7fb8ed75006dea419cf22850eb73a90cccb,
  token62f67e99a7c8decd. ACTUAL110e223...0ea7receiptbound; newtoken absent
  priorpmsg/latch+refusalguards verified;19backup hashes rechecked beforewrite.
- Guardedwriter starting onlyboot_b after finalserial/product/B/unlocked/
  firmwareFastboot/geometry/source/hash/backups gates. This line PRECEDESwrite;
  consult resetattention/phone-trial/state.json andflashlog forexactoutcome.
  No111physicalUA/TUR/capacity/block resultyet. Neverrestartwriter/controller;
  nooriginalrestore/protected/GPT/userdata/slotwrites; fullgoalunfinished.

## CURRENT0111 CI accepted; fresh native preflights LIVE (2026-10-20)

- CI39426515098/job118640347562 TERMINAL SUCCESS; cachedBuild188s,
  1069direct+2preprocessedhits/1miss. Artifact12266332483 ZIP SHA
  9a0dfcad0b1f3220134bcfb43fa0e0850339f7939c68755fdd4106c650a4b45b;
  exactcommit/ACE/cachedprovenance/SHA256SUMS/newreadinesslinkedstrings/entry/
  cacheCIVAC verified. Kernel17541576B SHA
  80f99dab8dcc2b86ecf17409a69a65951f555818c6cd83d810c5c8bb8f95ab49.
- ActualLINKEDfixedSMC ONEsmc/exactFID/op/high/zeroargs verified; complete CI
  log confirms111patch. Fresh native98662 LIVE9cases/Centry/4Android/package
  283tests. No111phonewriteyet; actual110e223...0ea7retained. Do not restart.
- Broadergoal check: existingroot imageHFS16GiB retained; oldSweetrootdriver
  Qualcomm/LUN0 assumptions cannot be copied to MTK/LUN2. Beforeuserdatawrite,
  mandatory independent no-/data diagnostic readout path still unimplemented;
  presentAndroid/Magisk/AEE workflow depends on/data. Read success alone does
  NOT authorize bypassing this concrete recovery dependency. Fullgoalunfinished.

## CURRENT0111 cached CI dispatched ONCE (2026-10-20)

- Local8a196cd; remote24b94d394f95c90f136c73b422aa7febe3b24cca.
  UIexactbranch/commitverified; ACE13.5DEVELOPMENT cached/diagnosticfalse,
  run39426515098/job118640347562 LIVE. Do not redispatch.
- Final283testsPASS58.395s/sixcompiles/SWEETunchanged/importsABI/exactsource+
  header/singleSMC PASS.19originalbackups and serial-bound expected physical
  firmwareFastboot product/B/unlocked/is-userspace=no reverified. No111image/
  phonewriteyet;actual110e223...0ea7retained. gh stillunauthenticated; existing
  connector/logged-inUI used/no credentials copied. Next exactartifact/fresh
  native/preflights/guardedboot_bonce/automaticv4trial. Fullgoalunfinished.

## ACTIVE HANDOFF: 0111 strict reset Unit Attention handling validated (2026-10-20)

- Previousgoalturn PROGRESS: actual110 fixed initQUERY completed and changed
  TUR LUN2 from05/25/00 to06/29/00. Expected firmwareFastboot/B/unlocked freshly
  identity-verified; actual110e223...0ea7 retained, no111phonewriteyet.
- Source111 classifies ONLY TUR LUN2 after device_init_complete, valid OCS/
  IS1/quiet HCS/requestCRC/guard and headeridentity/zeroresidual, response0or1+
  CHECK CONDITION2, fixed18-byte sense70/additional10/key06/ASC29/ASCQ00.
  Flags/EHS/unknown headers/lengths/sense/clock/reset changes refuse. This is
  notification return1, never data success. Dedicated one-shot readiness latch
  allows exactly one next TUR, requires GOOD before capacity/read. Repeated UA
  and other CHECK CONDITION now stop without generic inherited retry.
- Bounded response-prefix64 raw log on SCSI CHECK CONDITION/fault records any
  physically different sense format for further diagnosis. QUERYs retain log
  sampling; no media/reset/clock/firmware writes or extra retry added.
- Final283tests PASS58.395s; three new tests exercise exact response guards,
  actual command+readiness methods with timeout/OCS/UIC/CRC/guard/malformed/
  repeatedUA/unknownsense/noinit failures. Existing init methods/logbudget PASS.
  SixACE/SWEET compiles PASS/SWEET code+data+relocs unchanged/imports ABI,
  fuzz0fullpatchsource/header exact/singleSMC.19originalbackup hashes reverified.
- Next publish111/currentbranch cachedCI/diagnosticfalse ->exactartifact/
  freshnative+newtoken/native9+Centry+4Android/package283 ->guardedboot_bONCE/
  automaticv4withrefs/screen. Preserveactual110 until reviewedcandidate.
  Pipeline research/ace-ufs-resetattention-20261020. FullgoalACTIVE/unachieved.

## LATEST ACTUAL0110: device-init QUERY verified; reset Unit Attention next (2026-10-20)

- Writer73585/controller37702/offlineinspection/AEE67920 all TERMINAL SUCCESS.
  Actual retained boot_b64MiB SHA
  e223d3e47ce0d39f73ef79a28fc4f69fe596607dd1d64c9dacfc8bdaf8010ea7,
  tokena4791ca3b44829e0. DiagnosticADB76.1s/root/B/boot+vendor/currenttoken/
  automatic physical firmware Fastboot ready verified. No manualkeys/restore.
- NEW PHYSICAL: valid NOP/DMA again atPA142df4000. Fixed SET_FLAG query4:
  type36/response0/status0/opcode6/idn1/index0/selector0/value1 valid1;
  FIRST READ_FLAG query5 same valid fields/value0. fDeviceInit cleared after1
  reads. This establishes missing init handshake successfully performed.
- Subsequent TUR LUN2 NOW type21/OCS0/response1/status2/sense06/29/00, replacing
  previous05/25/00. RequestCRC unchanged, DBR0/HCSf/IE0/noUICerrors. Current
  command() rejects all response1 before classifying CHECK CONDITION, so stops.
  No capacity/block/GPT/root/media or usableiOS result. Never call UA success.
- Pinned ufshcd.c4978..5065 classifies CHECK CONDITION +copies sense after valid
  OCS/type. NEXT111 narrowly recognize actual reset Unit Attention06/29/00 in
  TUR only after strict complete header/identity/residual/sense-format+length/
  OCS/error/guard checks, consume ONCE, require next TUR GOOD before capacity.
  Unknown/malformed/other sense or repeated UA stops; do not generally ignore
  response1/errors. Add bounded raw response prefix logging so format guard
  failures remain diagnosable. No blind LUN scan or media/protected writes.
- Offline independent AEE55 entries CRC+size, rawring BYTEIDENTICAL16798B SHA
  137156991c5ad20cffbb9955ed3b5eb10a1e36c1e138ef7dd7c574e4e0143071;
  archive4da5afaf1c7c1b81d847ebd92942fe2332acc4b8070c4ec5a60659688c157ec7.
  First complete AEE tar15977984B SHA
  379595a95b80cdfae614fbeb9da371bac70cfa1713115d4a8cd874a7d3d89aec.
  Inspected phone screenshot Androidhome/USBfiletransfer20:49 only, NOTiOS.
- Source95c08e2/remote3706fd7 and CI39423623568/job118630527015 terminal;
  build201s/1071hits1miss, exactartifact12265018206/hash above accepted.
  109 artifact superseded before phone; no109trial exists. All processes now
  terminal/allREAclosed. Keep actual110 until reviewed fresh111 candidate.
  Full original iOS/display/touch/storage/basic-use goal ACTIVE/unachieved.

## CURRENT0110 written; automatic trial starting ONCE (2026-10-20)

- Writer73585 TERMINAL SUCCESS:onlyboot_b64MiB SHA
  e223d3e47ce0d39f73ef79a28fc4f69fe596607dd1d64c9dacfc8bdaf8010ea7,
  tokena4791ca3b44829e0; send1.428s/write0.172s/total1.602s.
  Finalidentity/B/unlocked/firmwareFastboot/geometry/source/hash/backups PASS.
- Automatic v4 controller startingONCE withrefs/screen/AEEintegrity. Actual
  initQUERY/flag-clear/LUN2 result UNKNOWN. Neverrestartwriter/controller.
  Nooriginalrestore/protected/GPT/userdata/slotwrites; fullgoalunfinished.

## CURRENT0110 packaged; guarded one-time boot_b write starting (2026-10-20)

- Native51778 TERMINAL SUCCESS9native/Centry/4Android/package280tests.
  Fresh64MiB candidate SHA
  e223d3e47ce0d39f73ef79a28fc4f69fe596607dd1d64c9dacfc8bdaf8010ea7,
  tokena4791ca3b44829e0. ACTUAL1080757...2482 receiptbound; newtoken absent
  priorpmsg/latch+refusalguards verified;19backup hashes rechecked beforewrite.
- Starting guardedwriter onlyboot_b after finalserial/product/B/unlocked/
  firmwareFastboot/geometry/source/hash/backups gates. This line PRECEDESwrite;
  consult initlog/phone-trial/state.json andflashlog forexactoutcome.
  No110physicalquery/LUNresultyet. Neverrestartwriter/controller; nooriginal
  restore/protected/GPT/userdata/slotwrites; fullgoalunfinished.

## CURRENT0110 CI accepted; fresh native preflights LIVE (2026-10-20)

- CI39423623568/job118630527015 TERMINAL SUCCESS; cachedBuild201s,
  1069direct+2preprocessed hits/1miss. Artifact12265018206 ZIP SHA
  4155ec1c3fc62edab30be1903e1fdeaa56b06b88e1ccb9a88ace7ee8a49f7c25;
  exactcommit/ACE/cachedprovenance/SHA256SUMS/newinitlinkedstrings/entry/
  cacheCIVAC verified. Kernel17541456B SHA
  5847874ea5be3622a1c196ad22617882475da5d1a3965e7dad25edb7de763d54.
- ActualLINKEDfixedSMC ABI ONEsmc/exactFID/op/high/zeroargs verified; complete
  CI log confirms109+110patches. Fresh native51778 LIVE9cases/Centry/4Android/
  package280tests. No110phonewrite yet; actual1080757...2482 retained.
  Neverrestartliveprocess/controller; full iOS goal unfinished.

## CURRENT0110 cached CI dispatched ONCE (2026-10-20)

- Local95c08e2; remote3706fd77e759e47ad967746945a27baae808691b.
  UIexactbranch/commitverified; ACE13.5DEVELOPMENT cached/diagnosticfalse,
  run39423623568/job118630527015 LIVE. Do not redispatch.
- Final280tests PASS52.033s/sixcompiles/exactpatchinput/SMC/header/ABI/SWEET
  PASS, actual300querylog<8KiB. Actual1080757...2482 retained;109 neverphone
  written. Await110exactartifact/nativepreflight/guardedboot_bonce/autotrial.
  No rollback/protected/GPT; full goal remains unfinished.

## ACTIVE HANDOFF: 0110 bounds poll logs; 0109 superseded BEFORE phone trial (2026-10-20)

- Found BEFORE phone write: up to300 healthy flag1 QUERYs with3logs each could
  overflow64KiB pmsg and erase the fresh token entry. No such physical failure
  claimed. 0110 logs first3/powers-of-two normal reads, EVERY fault and final
  readcount; every response still checked. No protocol/state/retry/timing change.
- Actual transport harness formats real printf strings; all300 flag1 reads plus
  SET+timeout total<8192B. Full280tests PASS52.033s; sixcompiles/SWEETunchanged/
  ABIimports/exactpatchsource/singleSMC PASS. Pipeline research/ace-ufs-initlog-
  20261020, prior ACTUAL1080757...2482 bound (109 never phone written).
- 109CI39422623191/job118627145049 TERMINAL SUCCESS cachedBuild190s,
  1069direct+2preprocessedhits/1miss. Artifact12265390267 ZIP
  e78906587c6eedc7d445582e246508ec5df3e1963b14b8598cc56dceacb5ba19.
  Exact downloaded provenance/metrics/hash/log retained deviceinit directory;
  superseded before native packaging/phone write; do not trial this artifact.
- Next publish0110/currentbranch cachedCI/exactartifact/freshnative/preflight/
  token/guardedboot_bonce/autotrial. Current108retained at firmware Fastboot.
  No newphonewrite/reboot/rollback/protected/GPT. Fullgoal ACTIVE/unachieved.

## CURRENT0109 cached CI dispatched ONCE (2026-10-20)

- Localdeef93a; remote b31eeb75ebf56b45ea805df4d992f77d7e14b2ea.
  UI exactbranch/commit verified; ACE13.5 DEVELOPMENT cached/diagnosticfalse,
  run39422623191/job118627145049 LIVE. Do not redispatch.
- Final280 tests PASS58.473s; sixcompiles/SWEETunchanged/ABIimports/exact
  patchheader+source/single SMC PASS. Rehashed19backups and serial-bound
  expected firmwareFastboot product/B/unlocked/is-userspace=no verified.
  No109image/phonewrite yet; actual1080757...2482 retained.
- gh auth still absent; existing connector/logged-in UI used, no credentials
  copied. Observation timeout resolved by same handle, no duplicate dispatch.
  Next exactartifact/nativepreflights/guardedboot_bONCE/v4automatictrial.

## ACTIVE HANDOFF: 0109 bounded fDeviceInit handshake locally validated (2026-10-20)

- Previous goal turn PROGRESS: physical0108 peer/NOP >4GiB DMA and new TUR
  LUN2failure05/25/00 established. Actual1080757...2482 retained at verified
  identity-bound firmware Fastboot/B/unlocked; no109phonewrite yet.
- 0109 adds fixed QUERY opcode6 SET_FLAG idn1/index0/selector0 once after NOP,
  then opcode5 READ_FLAG until value0 with1500ms/300read limit/5ms interval.
  Consumed latch before submit; no failed-command retry/descriptor/attribute/
  LU configuration/media writes. Requires accepted reset/known HW/clocks/link/
  quiet ownership/queue base before each query; echo/type/tag/response/length/
  value/requestCRC/DMA guard/OCS/IS/HCS validation. Stop before SCSI on fault.
- New host-tested header copied exact into patch; actual transport+poll methods
  exercised, dropped/malformed response, reset-change, DMA guard/requestCRC,
  timeout/endlessflag and one-shot refusal covered. Initial test corrected its
  mock deadline assumption (poll timer begins AFTER SET ack); no source guard
  weakened. Six ACE/SWEET compiles PASS/SWEET code+data+relocs unchanged,
  imports ABI checked; full fuzz0 patch input/header match and ONE SMC PASS.
  Full regression exact result private deviceinit/host-tests.log.
- Rehashed19 originalbackup hashes/deviceorigin sizes; firmware Fastboot
  product/B/unlocked/is-userspace=no verified. New source evidence includes
  pinned ufshcd.c init order and upstream v5.10 query struct byte layout.
  Next current-branch cachedCI/exactartifact/freshnative/newtoken/boot_bONCE/
  automatic v4 trial. All108processes terminal; no rollback/protected/GPT.
  Full usable iOS/display/touch/storage/system goal ACTIVE/unachieved.

## LATEST ACTUAL0108: real peer and NOP DMA verified; LUN2 not ready (2026-10-20)

- Writer82965/controller56445/inspection/AEE5577 all TERMINAL SUCCESS.
  Retained actual boot_b SHA
  0757ef192c64bda1051a811f6db123d6499fc2652705cc67e3b6068802b42482,
  tokenc6db1e863e3cd587; diagnosticADB76.1s, root/B/boot+vendor/currenttoken
  verified and automatic physical firmware Fastboot ready. No manualkeys.
- NEW PHYSICAL: accepted SIP/reset1, stopped XOUFS2->82/readback, HCE/UCRDY,
  one LINK_STARTUP rc0/HCSf/IS404 then quiet, local link UP, peer GET1561
  rc0/value2. Dedicated DMA PA142df8000; NOP OCS0/type20/response0/status0.
  Genuine peer response and >4GiB descriptor DMA/NOP now verified, not iOS.
- Next TUR LUN2 fails OCS0/type21/response1/status2/sense05/25/00; requestCRC
  unchanged, no UICerrors, DBR0/RSR1. No capacity/block/GPT/root/media result.
  Do not ignore response1, blindly retry TUR/LUNs or claim storage success.
  Driver currently omits UFS fDeviceInit completion after real device reset.
  Pinned ufshcd.c4374ff and7926ff explicitly NOP ->SET_FLAG fDeviceInit ->
  bounded READ_FLAG clear before LU discovery. This is the next source-backed
  initialization gap; unsupported-LUN response alone does not prove its cause.
- Independent AEE55entries CRC+size, raw ring byteidentical SHA
  c596f8b32edb9bf74aa21bf3dcfbd1c18dec7721abe16d8bf41a69af7a4283db;
  archive22607fc830a4f28ef4eb38a54e3ed5df669b4ec39f207c358ca9c8be1be0f5a7.
  Inspected screenshot Androidhome/USBfiletransfer20:18 only. No XNUdisplay.
- NEXT109 implement tightly bounded source-backed init QUERY flag handshake
  with exact wire/response guards, test/compile/cachedCI/freshnative/token/
  guardedboot_bONCE/autotrial; preserve108untilnextreviewedcandidate. No media
  writes/protected/GPT/rollback. Full iOS goal ACTIVE/unachieved.

## CURRENT0108 written; automatic trial starting ONCE (2026-10-20)

- Writer82965 TERMINAL SUCCESS: onlyboot_b64MiB SHA
  0757ef192c64bda1051a811f6db123d6499fc2652705cc67e3b6068802b42482,
  tokenc6db1e863e3cd587; send1.400s/write0.143s/total1.544s.
  Finalidentity/B/unlocked/firmwareFastboot/geometry/source/hash/backups PASS.
- Automatic v4 controller startingONCE withrefs/screen/AEEintegrity. Actual
  postreset XOUFS/HCE/startup/peer/NOP unknown. Neverrestartwriter/controller.
  Nooriginalrestore/protected/GPT/userdata/slotwrites. Fullgoalunfinished.

## CURRENT0108 packaged; guarded one-time boot_b write starting (2026-10-20)

- Preflight88802 TERMINAL SUCCESS9native/Centry/4Android/package276tests.
  Fresh64MiB candidate SHA
  0757ef192c64bda1051a811f6db123d6499fc2652705cc67e3b6068802b42482,
  tokenc6db1e863e3cd587. PriorACTUAL107f88a...fea5 receipt bound/newtoken
  absentpriorpmsg/latch+refusal guards verified; 19backup hashes rechecked.
- Starting guarded writer onlyboot_b after finalserial/product/B/unlocked/
  firmwareFastboot/geometry/source/hash/backups gates. This line precedeswrite:
  consult resetvendor/phone-trial/state.json andflashlog forexactoutcome.
  No108physicalresultyet. Neverrestartwriter/controller; retainexperiment,
  nooriginalrestore/protected/GPT/userdata/slotwrites; fullgoalunfinished.

## CURRENT0108 CI accepted; fresh native preflights LIVE (2026-10-20)

- CI39420009049/job118618316098 TERMINAL SUCCESS; build209s cached,
  1069direct+2preprocessed hits/1miss. Artifact12263213363 ZIP SHA
  2259a7ffef7f524f1959239bdb30b020afdafc824965a33c32c42510e22675d7;
  exact commit/ACE/cached provenance/SHA256SUMS/new linked strings/entry/cache
  CIVAC verified. Kernel17541208B SHA
  bb98bdeeb41cfc318d769069f7f67525bf6c7b2f5b71410660c70a11a53f2534.
- Actual LINKED firmware_release ONEsmc/exact FID/op/high/zero args verified.
  Native preflight88802 LIVE9cases/Centry/4Android/package276tests.
  No108phonewrite yet; actual107f88a...fea5 retained. Do not restart process.

## CURRENT0108 cached CI dispatched ONCE (2026-10-20)

- Local3704bb6; remote f420641f1ea18cb8a3a2b830c01e2a4ee4e9d761.
  Exact UI branch/commit verified; ACE13.5DEVELOPMENT cached/diagnosticfalse,
  run39420009049/job118618316098 LIVE. No108 image or phonewrite yet.
- Final276 tests PASS55.421s; six compiles/SWEET unchanged/ABI imports/
  patch input/single SMC PASS. 19original backups and serial-bound expected
  physical firmware Fastboot product/B/unlocked/is-userspace=no reverified.
  Actual107f88a...fea5 retained. Await exact artifact/native preflights/
  guarded boot_b once/automatic v4 trial. Do not redispatch/restart controllers.
- gh auth status still unauthenticated; existing GitHub connector/logged-in
  browser used, no credential copying. Screenshot ci-dispatch.png private.

## ACTIVE HANDOFF: 0108 stopped XOUFS restoration locally validated (2026-10-20)

- Source0108 follows pinned family/exact shipping hce_enable_notify ordering:
  after accepted SIP +10ms, stopped quiet HCE/HCS/RSR/DBR/IE/IS/AHIT0, HW36,
  AO gates enabled/reset1/refclk3/ownership checks, restore observed XOUFS2->82
  once; known82 requires no write. Unknown/change/readback failure stops before
  HCE. Recheck same context before/after; existing single startup/peer/NOP gates
  retained. No additional SMC/reset/power/crypto/storage writes.
- Four targeted actual-method/SMC ABI tests PASS; includes dropped vendor write,
  reset changing after write, gated clock/busy/unknown/missing ack refusal.
  Six ACE/SWEET singlefile compiles PASS; SWEET code/data/relocations unchanged,
  every import linked ABI checked, full fuzz0 patch reconstruction exact,
  actual controller ONE SMC. Full regression terminal result in private
  ace-ufs-resetvendor-20261020/host-tests.log. No108phone image/write yet.
  Actual107f88a...fea5 retained at firmware Fastboot; full iOS goal unfinished.

## LATEST ACTUAL0107: reset clears XOUFS enable bit; firmware Fastboot ready (2026-10-20)

- Writer98332/controller21238/offline inspection/independent AEE60700 all
  TERMINAL SUCCESS. Actual retained boot_b SHA
  f88a5ff798423c92edbcb37fae38945cb4c4841b66a3259c20f979376b19fea5,
  token60f9e8d67106f7dd. Diagnostic ADB78.1s; root/B/boot+vendor hashes,
  current-token evidence and automatic physical firmware Fastboot return verified.
- NEW PHYSICAL: SIP rc0, NS-AO90=1 stable; after10ms HCE/HCS/IE/DBR/RSR/
  AHIT/IS all0, REFCLK3, XOUFS2. Explicit stopped-state gate failed, no HCE
  enable/UIC/DMA. This establishes XOUFS82->2 during stop/reset; no longer a
  hypothesis. No electrical pin/peer/NOP/storage/iOS success claim.
- Independent AEE55 entries CRC+size verified; pmsg byte identical SHA
  b203c7fc05ed9484087e5f2e3ea92375f1908005892868a574dcf5f5d3c2f2ec;
  HWT archive5789914ba6d5bec864dc509ce73e99bb9ea59dedc51ea02a8606ed3033219bbf.
  Personally inspected screenshot: Android home/USB file-transfer picker only.
- NEXT0108: pinned family source and exact shipping hce_enable_notify both
  set XOUFS bit0x80 AFTER reset BEFORE HCE enable. Restore only known2->82
  under accepted one-shot SIP/reset/clocks/stopped/quiet gates, read back82;
  keep fail-closed gate, one HCE/startup and all peer/DMA checks. Fresh token,
  cached CI, native preflights, guarded boot_b once then automatic trial.
  No rollback/protected/GPT/userdata writes; full iOS goal ACTIVE/unachieved.

## CURRENT0107 written; automatictrial starting (2026-10-20)

- Writer98332 TERMINALSUCCESS:onlyboot_b64MiB SHA
 f88a5ff798423c92edbcb37fae38945cb4c4841b66a3259c20f979376b19fea5,
 token60f9e8d67106f7dd. Finalidentity/B/unlocked/firmwareFastboot/geometry/
 source/hash/backups gatesPASS; send1.383s/write0.145s/total1.530s.
- Automaticv4returnpolicy+AEEintegritycontroller startingONCE withrefs/screen;
 actualpostreleasegateconditionsUNKNOWN. Neverrestartwriter/controller.
 Nooriginalrestore/protected/GPT/userdata/slotwrites. Fullgoalunfinished.

## CURRENT0107 packaged; guarded one-time write starting (2026-10-20)

- Preflight99704 TERMINALSUCCESS9native/Centry/4Android/package275tests.
 Fresh64MiB candidate SHA
 f88a5ff798423c92edbcb37fae38945cb4c4841b66a3259c20f979376b19fea5,
 token60f9e8d67106f7dd. PriorACTUAL0106/2edb...b812bound; newtoken absentprior
 pmsg; latch/refusalguardsverified,19originalbackuphashes checked.
- Guardedwriterstarting onlyboot_b after finalidentity/B/unlocked/firmware
 Fastboot/geometry/source/hash/backups gates. Thislineprecedeswrite:consult
 sipsettle/phone-trial/state.json andflashlog forexactoutcome. No107physical
 settle-snapshotresultyet; neverrestartconsumedwriter/controller.

## CURRENT0107 CIaccepted; nativepreflights LIVE (2026-10-20)

- CI39418014291/job118611686597 TERMINALSUCCESS; cachedBuild192s,
 1069direct+2preprocessedhits/1miss. Artifact12263130788 ZIP
 65b191ffd431ff28035e158acd4b6694f798d804cbe5c407d42968b6c2496b14;
 exactcommit/ACE/cachedprovenance/SHA256SUMS/newsettlelinkedstrings/entry/
 cacheCIVAC verified. Kernel17541064B SHA
 d450be063d072715334bc7b6c82d4b233012c9dd12e88907a8184db37d21296d.
- ActualLINKED107firmware_release helper independently ONEsmc/exactFID/op/
 high/zeroargs checked. Nativepreflight99704 LIVE9cases/Centry/4Android/
 package275tests; no107phonewriteyet. Actual0106/2edb...b812retained.

## CURRENT0107 cached CI dispatched ONCE (2026-10-20)

- Local34ffc32; remote75fea461906e32a2d5ef08937c4a1dc87130a379. ExactUIcommit/
 branch confirmed; ACE13.5DEVELOPMENT cached/diagnosticfalse; run39418014291/
 job118611686597 LIVE. No107image/phonewriteyet. Do notredispatch.
- Final275tests/sixcompiles/exactpatchinput/ONEsmcPASS. 19originalbackups
 rehashed/device-originhashesaccepted; currentserial-bound firmwareFastboot
 product/B/unlocked/is-userspace=noPASS. Actual0106/2edb...b812retained.
 Privatepipeline sipsettleprepared; nextexactartifact/nativepreflights/
 guardedboot_bONCE/v4AEEintegritytrial tofindactualpostreleasegatefailure.

## ACTIVE HANDOFF: 0107 settled-state diagnostic validated (2026-10-20)

- Actual0106physicalSMCrc0/NSview1 acceptedrelease; subsequentstoplocation is
 control-flow inference untilnewreadouts, noHCEaftermeasurementyet. 0107 logs
 allpost10msgate inputs andexplicitfail/pass beforeHCEenable; noextraSMC/
 reset/clock/queue/storagewrites. Keepsallpreviousgates.
- Becauseactual106 provesNSview1observable afterSIP, removedzero-viewcompat
 andREQUIRE stable1 plusfirmwareack; firmwareackwithzero nowstopsbeforeHCE.
 This narrows toknownphysicalcontract, notchangingstartupsequence. Updated
 actualmethodfaulttests/clockguardtests. Final275testsPASS39.998s; sixACE/
 SWEETcompilesPASS/SWEETunchanged/importschecked/exactpatchsource/ONEsmc.
 Privatepipeline ace-ufs-sipsettle-20261020 prepared; priorreceiptactual0106
 2edb...b812. No107CI/image/phonewriteyet. NextcachedCI/exactartifact/native
 preflights/guardedboot_bONCE/v4AEEintegritytrial. Fullgoalunachieved.

## LATEST ACTUAL0106: firmware release succeeds; post-settle gate stops (2026-10-20)

- Actualboot_b64MiB SHA
 2edbaa0c920e5bd1072cadcd5becaf3eb28438628189348cd40fe9bdbe9bb812,
 tokenf04660cff7d56edf. Writer18506/controller70395 TERMINALSUCCESS;
 ADB76.1s/root/B/boot+vendorreadbackverified, refs/logs/screen, automatic
 expectedphysicalfirmwareFastboot return. Retain0106, nooriginalrestore.
- KEYNEWPHYSICAL: exactSMCc2000276/op2/high1 returnedrc0; AO90 NSview0->1.
 Lists/HCEstopped. Onefirmwarecall only; noNSresetstore. This confirms release
 controlisobservablethroughSIP onactualphone, notmerelyRAZ. Electricalpin and
 peerlink stillnotdirectlyproved. Lastlogacceptedreleasecommand; noHCEenable/
 UIC/startup/peer/DMAlogs. Driver has silentpost10ms gate onview/HCE/DBR/IE/
 REFCLK/XOUFS; exactfailedconditionUNKNOWN. Likely resetclearsXOUFS82 is only
 a hypothesis; doNOTremovegate orrepeatidenticalcandidateblindly.
- NewAEEintegritycollection physicallyPASS firstattempt16211456B complete,
 SHA85dec73a451d0cbe91e3f15c9c7378c8027bb9b1a13ac5c5aba35b9a3244d371.
 Independent14782 TERMINALSUCCESS55entriesCRC+size; rawringbyteidentical,
 pmsg9395B SHAc4915f091d50abd22248ed5c1d6e85ae8cd01fd48678e98b260379552ff61040;
 HWTarchive dcc462ec7cbe8aaa6d2ee4d14e80436a9941363f4b05d95400dca668e8d5781f.
 WatchdogCPU0PC7491a9c maps cpu_idle; notnew UFS exceptionproof. Screenshot
 personallyinspected Androidhome+USBpicker/filetransfer, NOTiOSdisplay.
- NEXT0107 addreadonly loggedsnapshot of everypostrelease10msgate input and
 explicitstopreason beforeHCEenable; preserveallchecks/noextraSMC/startup/
 hardwarewrites. Establishwhichstateactuallychanged, thenfixthatdiscrepancy.
 All106processes/CIterminal; allREAclosed. FulliOSgoalACTIVE/unachieved.

## CURRENT0106 written; automatictrial starting (2026-10-20)

- Writer18506 TERMINALSUCCESS:onlyboot_b64MiB SHA
 2edbaa0c920e5bd1072cadcd5becaf3eb28438628189348cd40fe9bdbe9bb812,
 tokenf04660cff7d56edf. Finalidentity/B/unlocked/firmwareFastboot/geometry/
 source/hash/backups gatesPASS; send1.385s/write0.137s/total1.524s.
- V4returnpolicy controller+newAEEintegrityreads startingONCE withrefs/screen.
 ActualSMC/NSview/HCE/startup/peer/NOPunknown. Neverrestartwriter/controller.
 No originalrestore/protected/GPT/userdata/slotwrites; fullgoalunfinished.

## CURRENT0106 packaged; guarded one-time boot_b write starting (2026-10-20)

- Preflight51193 TERMINALSUCCESS9native/Centry/4Android/package275tests.
 Fresh64MiB candidateSHA
 2edbaa0c920e5bd1072cadcd5becaf3eb28438628189348cd40fe9bdbe9bb812,
 tokenf04660cff7d56edf. PriorACTUAL0105c435...dac0bound; newtoken absentprior
 pmsg; pendinglatch/refusalguardsverified. 19originalbackuphashes verified.
- Guardedwriterstarting onlyboot_b after finalserial/product/B/unlocked/
 firmwareFastboot/geometry/source/hash/backups gates. Thislineprecedeswrite:
 exactresult sipreset/phone-trial/state.json andflashlog. No0106physicalSMC/
 link/peer/NOP resultyet. Nextv4controllerwithAEEintegrity+screenshots, ONCE.

## CURRENT0106 CIaccepted; freshnativepreflightLIVE (2026-10-20)

- CI39415860151/job118604578683 TERMINALSUCCESS; cachedBuild179s,
 1069direct+2preprocessedhits/1miss. Artifact12262096719 ZIP
 6960f2bf87f9e39504035a25cdfd64e4625079c6758101c80622c395e8611941.
 Exactcommit/ACE/cachedprovenance/SHA256SUMS/newlinkedstrings/entry/cacheCIVAC
 verified. Kernel17541064B SHA
 c99d1d9ccd78609d37a3ea3174170c9d236555ff573161604a312af7737230dc.
- ActualLINKEDfirmware_release_device disassembly independentlychecked:
 ONEsmc exactFIDc2000276/x1=2/x2=1/x3..7=0. Savedlinked-firmware-release-
 disassembly.txt; this isstaticABIproof, NOTphysicalSMCsuccess.
- Nativepreflight51193 LIVE9cases/Centry/4Android/package275tests. No0106
 phonewriteyet. Actual0105c435...dac0retained; donotrestartprocess.

## CURRENT0106 exact cached CI dispatched (2026-10-20)

- Localae31c5b; remote5ae4743462b523fbe5d03dc405779875a336ca3b. DispatchedONCE
 ACE13.5DEVELOPMENT cached/diagnosticfalse; run39415860151/job118604578683,
 exactbranch/commit shownUI, currentlyqueued/live. Do not redispatch.
- Full275tests/sixcompiles/actualONEsmcABI/exactpatchinputPASS. All19original
 backups rehashed againstdeviceoriginbefore/stream/after; currentserial-bound
 expectedfirmwareFastboot product/B/unlocked/is-userspace=noPASS. Actual0105
 c435...dac0retained; no0106candidate/phonewrite/SMCyet. Awaitexactartifact+
 native9/Centry/4Android/package275 ->guardedboot_bONCE ->v4AEEintegritytrial.
- gh stillunauthenticated; existingconnector/logged-inUI fallback used; no
 credentialscopied. UIobservationtimeout resolvedsamehandle, no duplicateCI.

## ACTIVE HANDOFF: 0106 exact SIP device-release candidate locallyvalidated (2026-10-20)

- Previousgoalturn PROGRESS: actual0105 showedNSreleasewrite unobserved and
  preservedfirmwareFastboot; fixedAEEtarreadguards and auditedexactSIPservice.
  Currentinstalled0105c435aecacfabb4764d8eedf35fac1ed4665408f93a8afed90197dfd74710dac0,
  tokenb89f8e99f96ac9d9. No newphonewrite/SMC yet; allpriorprocessesterminal.
- Source0106 removesNSresetstore/RWmapping. KnowninitialAO90=0/clocks/HW36/
  quietownership/HBAstop gates ->onefixedSMCc2000276,2,1,0..0 only; SMCCC
  x0..17clobbercontract, onlyrc0accepted; noassert/power/crypto/versionguess.
  NS0or1recordedafterack; unknown/change stops. NS0admissibleONLYwithcurrent
  acceptedoneshotfirmwarecall, nottreatedas electricalpinproof. Existingone
  HCEenable/prelink/startup/quietUP/peer/NOP gatesremain; noerrorignore/retry.
- Final275hosttestsPASS36.815s; new3tests exerciseactualmethods withonlySMC
  instruction/registerbindingmocked, everywait/UIC/map/rc/unknown/change/
  clock/ownership/one-shot boundary; actualARM64helperABIcompiled/disassembled.
  SixACE/SWEETcompilesPASS/SWEETcode-data-relocsunchanged/importschecked.
  Actualfull driverobjectcontainsONEsmc; fuzz0patchsequenceexactsourcehash
  matchescompiledinput. Privateproofs/pipeline ace-ufs-sipreset-20261020.
- Nextpublishcurrentbranch/cachedCI/diagnosticfalse ->exactartifactaccept ->
  freshnative9/Centry/4Android/package275tests, rehash19backups/identity,
  bindACTUAL0105receipt/newtokenabsent ->boot_bONCE ->v4returnwithAEEintegrity
  guardedreads+screenshots. Neverrestartconsumedwriter/controller. Goalunachieved.

## NEXT0106: exact firmware reset-release service audited; no newcandidate yet (2026-10-20)

- Same actual0105c435aecacfabb4764d8eedf35fac1ed4665408f93a8afed90197dfd74710dac0
 tokenb89f8e99f96ac9d9 retained, lastphysicalfirmwareFastboot from verified
 auto-return; no additionalphoneIO/reboot/write/SMC. FullgoalACTIVE/unachieved.
- ExactATF082d...1724 service descriptor at raw3e600 binds c2000276/82000276
 to0x48229660, nameMTK_SIP_KERNEL_UFS_CONTROL,indexptr482412de. REAbytes
 ev_6463b6...b9fc +pseudocode ev_9af85f...a16f +assemblyev_574f19...0cd0 prove
 subop2/nonzeroarg setsAO112b8090bit0 andx0=0return, preservingotherbits.
 Raw-newbase query had noidentifiedfunction; did NOTinvent decompilation.
 Analysis-onlyELF wrappera2b9...708c preserves EXACT289656B originalpayload;
 onlyanalystlabels/headers at independentlydecodedprologues. Evidence+snapshot
 underresetinit/atf-exact-reset-service-evidence.json and
 rea-atf-reset-analysis-elf-snapshot.json. AllREA sessions CLOSED/queriesterminal.
- Next implement106 exact bounded SMC(FIDc2000276,x1=2,x2=1,x3..7=0), after
 knowninitialHW/clock/ownership/quiet/HBAstop/10uslow gates; noadditionalNS
 AO90write and noassertpulse. PreserveSMCCC x0..17clobbercontract, acceptonly
 rc0, lograwreturn+NSview, settle10ms, thenboundedexistingoneHCE/oneinitpath.
 NSviewmayremainRAZ: commandack is NOTpin/linkproof; justify/qualifyNS-view
 gatingexplicitly and requirefreshUICstartup/quietUP/peer/NOP, neverignore
 errors or repeatSMC/startup. No0x80power/versionguess/PHY/PLL/protectedwrites.
 Faulttest rcerror/readbackunknown/change/oneshot/allcompletionfaults andcross-
 compileactualSMCregistercode beforecachedCI/currentbranch. Freshnative9/Centry/
 4Android/package272+tests/priorreceiptactual0105 thenboot_bONCE+v4returnflow.
- Controller AEEintegrityfix committed5309a99, full272testsPASS49.592s. Its
 versionmetadata nowtransport-refresh-v4-screen-aee-integrity; serial/token/
 rebootreturnpolicy unchanged. Newcollectionhelper notyetphysicallytested;
 retainall3attempts/flagincomplete ifneeded. Historical0105controller SHA
 verified againstgitd85f5c7 version, notthechangedcurrenttool. NofalseAEE55claim.
- Currenttree has nokernel106patch/CI/imageyet. Kernel105270tests/provenance
 remainhistoricalvalid; currenthost272tests includeAEEguards. Await next work.

## Automatic AEE archive validation repaired; reset SIP audit ongoing (2026-10-20)

- Added complete_tar +bounded3 identity-refreshed AEEreads toauto-trial;
  retain every rawattempt/hash/validity observation and markincompleteafter3,
  continue guardedFastbootreturn withoutrebootretry. Completeness is container
  only, notcurrenttoken/ZIPCRC proof. Testknownactual0105tar rejected and0104
  accepted. Twoactualhelpertestscovertruncation/corruption/size/footer/refresh/
  retention/exhaustion/unverifiedtransport. Full272testsPASS49.592s. No deviceIO
  for thisfix; actual0105/automaticcontroller alreadyterminal/notrestarted.
- OfflineATFdescriptor0x3e600 contains handler0x48229660,FIDs82000276/c2000276,
  nameMTK_SIP_KERNEL_UFS_CONTROL at0x4823b703,indexptr0x482412de. Indexinitial-1
  is runtimeinitialized, NOTproofserviceabsent. Jump-table subop2->0x296ec
  toggles112b8090bit0 basednonzeroarg. Exactbytes/identity inresetinit/
  exact-reset-sip-binding.json. Existing shippingmodule/source callsFID,2,1
  forresetrelease, withstop/10uslow/10mssettle. NoSMCexecutedyet.
- OpenedsameATF082d...1724 inREA with0x48200000rawmapping inferredfromactual
  descriptor pointers, to recover exacthandler omitted atoldbase0. Query149
  LIVE; next readitsresult/exportevidence/closewithsnapshot. Do notduplicate
  analysis. Currentdevice remains0105c435...dac0 inverifiedfirmwareFastboot.

## LATEST ACTUAL0105: ordinary reset-release write not observed (2026-10-20)

- Actualboot_b64MiB c435aecacfabb4764d8eedf35fac1ed4665408f93a8afed90197dfd74710dac0,
 tokenb89f8e99f96ac9d9. Writer83917/v4controller37673 TERMINALSUCCESS;
 ADB78.1s/root/B/boot+vendorhashreadback verified, refs/pstore/dmesg/screen
 captured, automaticexpectedphysicalfirmwareFastboot returned. Retain0105.
- NEWPHYSICAL: clocks enabled/quietUP2host1; lists/HCEstop verified. ONE NS
 AO90release write sent1 but exactreadbackstill0. DriverSTOPPED immediately
 beforeHCEenable/UIC/startup/peer/DMA. No exceptioninlog, noSMCexecuted. This
 establishes NSwrite-not-observed; does NOTprove electricalpinlow or that
 NSread isn't RAZ. Possible secure-only/permission/firmware ownership remains
 inference. Do NOTrepeat thisNSwriteexperiment or relaxintoNoponoldUP.
- pmsg SHA9a48a38b3bf5c9a3217ab3564f43d76e7ae2cf7f834544248497bf1586648133. All savedartifactbytes match readout
 receipt. Screenshot personallyinspected Androidhome+USBpicker, notiOS.
- AEE archive actuallyTRUNCATED:9105920B, currentHWT header3273563B at6519808,
 available2586112B; incomplete beforetarEOF. Initialofflineparser raced live
 controller observation, rechecked AFTERterminal: sameincompletetar. No55entry/
 independentAEE claimthisboot. Preserveoriginalpartialarchive; phonealready
 Fastboot, noextra reboot/reruncontroller. Next automaticcollection needs
 bounded identity-refreshed archivevalidity rereads with allobservations kept.
- Next resetcandidate should use exact shippingSIPc2000276/subop2/high1 only
 afterexistingknownstate/HBAstop gates, notguessedpower/version/PHY. Before
 executing, auditATF dispatch/source/preservedbinary arguments; NSreadback may
 remainRAZ so distinguish firmwareack vs actualpin/link. Requirequiet bounded
 singlelocalstartup and genuinepeer/NOP proof; noblindresetretries/ignoredfault.
 Fullgoalstorage/root/display/touch/iOSstillunachieved. All105processesterminal.

## CURRENT0105 written; v4 automatictrial starting (2026-10-20)

- Writer83917 TERMINALSUCCESS:onlyboot_b64MiB SHA
 c435aecacfabb4764d8eedf35fac1ed4665408f93a8afed90197dfd74710dac0,
 tokenb89f8e99f96ac9d9. Finalidentity/B/unlocked/firmwareFastboot/geometry/
 source/hash/backups gatesPASS; send1.377s/write0.155s/total1.534s.
- V4controllerstarting ONCE withrefs/screenshots; actualreset-release/HCE/
 startup/peer/NOPunknown. Neverrestartwriter/controller. No originalrestore/
 protected/GPT/userdata/slotwrites; retainexperiment/fullgoalunfinished.

## CURRENT0105 packaged; guarded one-time boot_b write starting (2026-10-20)

- Preflight87922 TERMINALSUCCESS:9native/Centry/4Android/package270tests.
  Fresh64MiB candidate SHA
  c435aecacfabb4764d8eedf35fac1ed4665408f93a8afed90197dfd74710dac0,
  tokenb89f8e99f96ac9d9. Prioractual0104d693...6833bound; newtoken absentprior
  pmsg; latch/refusalguardverified;19originalbackups rehashed/identitychecked.
- Guardedwriterstarting onlyboot_b, finalserial/product/B/unlocked/firmware
  Fastboot/geometry/source/hash/backups gates first. This lineprecedeswrite:
  exactoutcome resetinit/phone-trial/state.json andflash-candidate.log. No0105
  physicalreset/startup/peer/NOP resultyet. Neverrestartconsumedwriter/controller.

## CURRENT0105 CI accepted; freshnativepreflight LIVE (2026-10-20)

- CI39412254010/job118592627571 TERMINALSUCCESS; cachedBuild215s,
 1069direct+2preprocessedhits/1miss. Artifact12260626241 ZIP
 9eb6e85d44ac0300cc60b946309d926a4410a95f8b37b096f665355b40b50927.
 Exactcommit/ACE/cachedprovenance/SHA256SUMS/reset-initlinkedstrings/entry/
 cacheCIVAC verified. Kernel17541000B SHA
 881f6cbbbd48cc2567eff0ab920d5a696f10d46e5972fe425e58ad8adb58df7d.
- Nativepreflight87922 LIVE: freshnative9/Centry/4Android/package270tests.
 Do not restartprocess; no0105phonewriteyet. Actual0104d693...6833retained.

## CURRENT0105 exact cached CI LIVE (2026-10-20)

- Localc7e4c54; remote c25e18efc10f59928a1cf05468636f4dc5575d00.
  DispatchedONCE ACE13.5DEVELOPMENT cached/diagnosticfalse; run39412254010/
  job118592627571 LIVE, exactcommit shownbyUI. No0105image/phonewriteyet.
- Final270tests/sixcompiles/exactpatchmatchesPASS. 19originalbackups rehashed
  againstbefore/stream/afterdevice-originmanifest; identity-bound expected
  physicalFastboot product/B/unlocked/is-userspace=no confirmed. Actual0104
  d693...6833 retained. AwaitexactCIartifact/freshpreflights/guardedboot_bONCE/
  v4automatictrial; no resetreleasehashwriteuntilconcreteimagechecks.

## ACTIVE HANDOFF: 0105 bounded device release/cold init validated (2026-10-20)

- Previousgoalturn PROGRESS: actual0104 proves AO90releasebit0; currentexact
  boot_b d693de51b498b575544d5b9714c74bf3fa08b85f4a858429ed83ab29b25d6833,
  token6c3de4148f42c75e, verifiedautomaticfirmwareFastboot return; no newwrite.
- 0105 implements source-backed recovery ONLY for exactAO90=0, knownHW36,
  quiet ownership/stable enabledclocks/refclk/XOUFS82 and idlequeues. Stops
  lists/HCE, verifiesstop, >=10uslow, ONE releasebitwritepreservingotherbits,
  exactreadback,10mssettle,HCEenable+600us, boundedlocalUICready separately
  fromDP; prelink controls +oneLINK_STARTUP thenquiet/UP/fullready/clockchecks,
  thenexistingonepeer/NOPpath. Alreadyreleasedpathdoesnotreset. Noassertion
  pulse/SMC/vendorreset/PLL/PHY/gear/powermode/storagewrites or automaticretry.
  HCEcyclewithoutfullvendorreset is boundedexperiment, notprovenhardwarefix.
- New actualmethod harness injects everywait/UICfault/map/stop/release-readback/
  resetstatechange/clock/ownership/unknownvalue/oneshot fault. Final270tests
  PASS44.182s; sixACE/SWEETsinglefilecompilesPASS/SWEETcode-data-relocsunchanged,
  everyimportmatcheslinkedABI. Fuzz0patchsequence exactlymatchescompiledsource.
  Private source/proofs/pipelineunderace-ufs-resetinit-20261020. Nextpublish
  cachedCI(currentbranch),exactartifactaccept+freshnative9/Centry/4Android/
  package270tests;priorreceiptmustbindactual0104; guardedboot_bONCE ->v4trial.

## LATEST ACTUAL0104: device reset release bit LOW; next bounded cold init (2026-10-20)

- Actualinstalledboot_b64MiB SHA
  d693de51b498b575544d5b9714c74bf3fa08b85f4a858429ed83ab29b25d6833,
  token6c3de4148f42c75e. Writer28611 andv4controller1704 TERMINALSUCCESS.
  ADB78.2s/root/B/boot+vendorhashreadback verified, refs/logs/screenshot saved;
  automaticexpectedphysicalfirmwareFastboot return. Retain0104, no routine
  originalrestore orrecoverypending. Original19backups intact/rehashed.
- KEYNEWPHYSICALRESULT:AO90=00000000/00000000 release-bit0/0, while stable
  selectedPROBE21100001/21100001 link2/host1 andlocalmode11/gears4/4. This
  samples the bit controlled by exactLK/ATF device-reset paths. Driver stops
  beforeadditionalLPM/peer/DMA; no reset/SMC executed. CachedhostUP is NOT
  usablepeerlinkproof. Pin electrical level/devicepower still not directly
  measured; do not claim every storagefailure is conclusivelyexplained.
- IndependentAEE2775 TERMINALSUCCESS55entriesCRC+size; rawringbyteidentical,
  pmsgSHA29b66ee7af0a3bcdc35d25e095536232dc5d5d1f1439c3b5ca0528dcaedbbaf8,
  archive286535c02d9fa2c3d88ff4035c6e95ffd5dc0acd6bd873133005d5cd24c35a64.
  Screenshot personallyinspected:Androidhome+USBpicker/filetransfer, NOTiOS.
  0103/0104CI/writers/controllers/preflights allterminal. AllREA sessionsCLOSED.
- NEXT0105 should implement one bounded SOURCE-backed coldinitialize ONLY
  afterrequalifying known HW/clock/ownership/quiet and the actualassertedreset.
  Shippingreference device_reset firststopsHBA, holdsresetlow>=10us, releases,
  waits10..15ms; HCE_PRE followsMTKreset/600us contract. Need explicit local-UIC
  readiness separatefromDP/queuefullreadiness duringcoldstartup. Preserve AO90
  otherbits and exactreadback; no blindtoggles/startupretries/errorignore/SMC
  or guessedPHY/PLL recipe. A resetrelease alone is not negotiatedlinkproof.
  Implement/faulttest/crosscompile/exactpatchcheck first; cachedCI/currentbranch,
  fresh token/native9/Centry/4Android/package269+ tests then guardedboot_bONCE
  andv4 automatictrial. Bind priorreceipt toACTUAL0104d693...6833,newtokenabsent.
- Remainingfullgoal: genuineNOP ->LUN2capacity/read-onlyGPT ->boundeduserdata
  rootdevice/APFS/launchd ->real display+touch/basicoperations+persistence.
  None of storage/root/display/touch/usableiOS verified. GoalACTIVE/unachieved.
- BrowserUI finalsummarysuccess read for0104, screenshotcapture twice timedout;
  existing0103CI screenshot preserved. Phone screenshots succeeded/inspected.

## CURRENT0104 written; automatic v4 trial starting (2026-10-20)

- Writer28611 TERMINALSUCCESS:onlyboot_b64MiB SHA
  d693de51b498b575544d5b9714c74bf3fa08b85f4a858429ed83ab29b25d6833,
  token6c3de4148f42c75e. Final identity/B/unlocked/firmwareFastboot/geometry/
  source/hash/backups PASS;send1.378s/write0.147s/total1.527s.
- V4controller starting ONCE withrefs/screenshots. ActualAO90resetbit unknown;
  inspect currenttokenlogs and AEE. Never restart consumedwriter/controller.
  No originalrestore/protected/GPT/userdata/slotwrites; fullgoalunfinished.

## CURRENT0104 packaged; one-time write starting (2026-10-20)

- Preflight68001 TERMINALSUCCESS9native/Centry/4Android/package269tests.
  Fresh64MiB candidateSHA
  d693de51b498b575544d5b9714c74bf3fa08b85f4a858429ed83ab29b25d6833,
  token6c3de4148f42c75e. Prioractual0103a282...6b71b bound; newtoken absent
  priorpmsg, retainedresetlatch/refusalverified;19originalbackups rehashed.
- Guarded writer starting onlyboot_b after finalserial/product/B/unlocked/
  firmwareFastboot/geometry/source/hash/backups gates. This precedeswrite:
  consult devreset/phone-trial/state.json and flash log for actualoutcome.
  No0104physicalreset sampleyet; no duplicate writer/controller/recovery.

## CURRENT0104 CI accepted; native preflights LIVE (2026-10-20)

- CI39409833937/job118584595241 TERMINALSUCCESS; cachedBuild201s/UI4m58s;
  1069direct+2preprocessedhits/1miss. Exactcommit/ACE/provenance/SHA256SUMS/
  linkedresetstrings accepted. Artifact12259600621 ZIP
  0fe7a239793822236603e45ad1958a6ee442050a57d1d202143cb7462c122b5d;
  kernel17540800B SHA9406a80cd4deea5d03f23b6065abf1dff09d87f56955b8626f5adca2b1532b01.
- Preflight68001 LIVE freshnative9cases/Centry/4Android/package269tests;
  do not restart. All19backups rehashed again. Prioractual0103retained;
  no0104phonewriteyet. Next guardedboot_bONCE ->v4automatictrial.

## CURRENT0104 readonly reset diagnostic cached CI LIVE (2026-10-20)

- Local305db10; remote0160a27f595144e162826a6ea40bb63682870690. Final269tests
  PASS41.500s; sixACE/SWEETcompilesPASS/SWEETunchanged/importschecked/exact
  patch reconstruction fuzz0. One readonly AO90release guard, no new writes.
- Dispatched ONCE cached/diagnosticfalse ACE13.5DEVELOPMENT; run39409833937/
  job118584595241 LIVE. Private pipeline devreset prepared; actual prior0103
  a282...6b71b; no0104image/writeyet. Await artifactaccept/freshpreflights/
  guardedboot_bONCE/v4automaticlogs+screen+independentAEE. Goalunachieved.

## NEXT0104: exact LK deinit reset lead; local validation LIVE (2026-10-20)

- New shipping-static chain on hash-pinned LK nativeVA ELF3c60...4c5a:
  finaltransition26ff0 ->platformcleanup02b5c ->UFSdeinit458a8 ->poweroff440d4
  and43d88. Last helper clears UFS-AO+90 bit0 for observed bootmode branch,
  else SMCc200040d/subop2/0. Evidence d1bf6a...895b /175fee...6fa9 /
  40a7b4...5d63 /f9cb8b...f1cc9. Bootmode-specific path and livebit unknown.
- ATF082d...1724 static handler2950c toggles same112b8090bit0; Linux UFS
  control29660 subop2 jump-table resolves296ec, samebit. Independent objdump
  and pinned device_reset_ctrl(high) identify low assert/high release. Ghidra
  has no29660procedure (explicitunknown), not fabricated decompilation.
- GenericPHY binding absent in actualFDT; exact shippinginit tolerates missing
  PHY, so never apply mt8183 PHY register recipe at guessedbase. Saved shipping
  power Evidence+snapshot and LK/ATF snapshots inlpmclock; REA sessions CLOSED.
- Source0104 only READS AO+90twice through existing readonly map and refuses
  furtherUIC/DMA if releasebitlow. No reset/SMC/PHY/gatewrites added. This tests
  concrete stale-UP-after-LK-reset hypothesis; notproven untilphysicalsample.
  Private devreset directory; compile/tests65237LIVE. Actualphone0103 retained.

## LATEST ACTUAL0103: clocks/LPM qualified; peer rc08 persists (2026-10-20)

- Actual0103boot_b SHA a2825e5ab53fac08bac79e7e0a172d1732a997bc046aadc6090fa91a6be6b71b,
  token2cb43d24b16b84f2. V4controller56833 TERMINALSUCCESS:ADB76.1s/root/B/
  boot+vendor readback verified; refs/logs/screenshot saved; automatic expected
  physical firmwareFastboot returned. Retain0103; no originalrestore.
- NEWPHYSICALOBSERVATION: AO/PDN00000000 twice; TOP0=02020202,TOP14=01030307
  stable. Selected gates enabled, not frequency/PLL/PHYproof. UniPro d0a8=0,
  d0a6=90 before/after, changed0: NO LPM SET issued. UP2/host1 and quiet error
  snapshots before/after. One peer1561 completesrc08 in2457232ticks,IS400,
  HCS10f; all5errorwords zero; selectedUP2/host1 persists. Invalidfailed value9a
  is NOT lane count. No DMAallocation/queue/NOP. Not a storage/root success.
- IndependentAEE31323 TERMINALSUCCESS55entriesCRC+size; rawring byteidentical,
  pmsg10727B SHA9d9efce415876f51e069b86f99d06b44d130d32d1c9b7f1984860043bcefaa19;
  archive5a585ed5fc6622d7887f31fc175d2b644c427e0edcc75fc4098c74b1e373cfd9.
  Screenshot inspected:Androidhome+USBpicker/filetransfer; not XNUdisplay.
- This narrows simple gated-clock/LPM/deepstall hypothesis on this boot, not
  all analogclock/PHY/devicepower/firmwareownership. Next investigate exact
  shipping PHY/devicepower/init/firmware handoff; do not repeat AUTO or rc08
  experiment without a concrete new discrepancy. FulliOSgoal stillunachieved.

## CURRENT0103 written; v4 automatic trial starting (2026-10-20)

- Writer15210 TERMINALSUCCESS:onlyboot_b64MiB SHA
  a2825e5ab53fac08bac79e7e0a172d1732a997bc046aadc6090fa91a6be6b71b,
  token2cb43d24b16b84f2. Sending1.397s/Writing0.141s/total1.540s; final identity/
  B/unlocked/firmwareFastboot/geometry/hash/source/backups gatesPASS.
- V4controller starting ONCE withreference snapshots/screenshots; actual
  clock/LPM/peer/NOP results unknown. Do not restart consumed writer/controller.
  Retain experiment; no originalrestore/protected/GPT/userdata writes.

## CURRENT0103 packaged; guarded one-time write starting (2026-10-20)

- Preflight82776 TERMINALSUCCESS:9native/actualCentry/4Android/package269tests.
  Fresh64MiB candidate SHA
  a2825e5ab53fac08bac79e7e0a172d1732a997bc046aadc6090fa91a6be6b71b,
  token2cb43d24b16b84f2; prior actual0102/db68...e663 receipt bound. New token
  absent priorpmsg; auto-readout latch/refusal and all19originalbackups verified.
- Guarded writer about to run onlyboot_b, final identity/B/firmwareFastboot/
  unlocked/geometry/source/hash gates first. This line precedes write; exact
  result in phone-trial/state.json and flash-candidate.log. No0103physical
  result yet; never restart consumed writer/controller. Next v4 auto trial.

## CURRENT0103 CI accepted; fresh native preflight LIVE (2026-10-20)

- CI39407303533/job118576244177 TERMINALSUCCESS; cachedBuild132s, UI3m12s,
  1069direct+2preprocessedhits/1miss. Artifact12257488631 ZIP
  fcef267fba9540ea8cd1a54317906d0ede2026a54bfda87cf28cc7edb68882ff;
  exact provenance/SHA256SUMS/new clock-LPM strings and absence failed AUTO
  strings accepted. Kernel17540800B SHA
  fe50480512c60f15c9c8338f79a2f33495a4dac820d79da4e7f9b9fca8b085a3.
- Native preflight82776 LIVE: first invocation refused missing ADT before any
  output/image or phone IO. Copied exact hash-checked prior unchanged ADT;
  fresh native bundle now built and9native/Centry/4Android tests in progress.
  Continue this process; do not restart it. No new phone writes yet.

## CURRENT0103 exact cached CI LIVE (2026-10-20)

- Localcommit cd66698; remote final e9dedc3a5868ba0fc5810c9f62f9156062bfc572
  (remote already had earlier0103; fetched blob and updated quiet gate exactly).
  Dispatched ONCE cached/diagnosticfalse ACE13.5DEVELOPMENT via existing UI;
  run39407303533/job118576244177 currently running. No new phone image/write.
- Final269hosttests and six cross-compiles passed; private pipeline prepared
  under ace-ufs-lpmclock-20261020. All19originalbackups rehashed; expected
  serial-bound Fastboot present. Prior receipt binds actual0102/db68...e663.
  Await exact CI; never restart dispatch/writer/controller blindly.

## ACTIVE HANDOFF: 0103 clock/LPM candidate locally validated (2026-10-20)

- Resumed existing full usable-iOS goal; it remains ACTIVE/unachieved. Actual
  phone remains0102/db68eb004cdfadaceab341d6ccc8f6e7569165f79c5cc1680965d4f52311e663,
  token0b27a6ed9f4f8b25, last verified firmwareFastboot; no new device write.
- Reviewed pre-existing untracked0103 + fault tests. Removed failed FASTAUTO
  experiment; read-only AO/PDN/top clock status from actual FDT/pinned family
  source; only when supported stable enabled gates, ownership/quiet/UP and
  valid local attributes permit, conditionally clear asserted UniPro LPM/deep
  stall bits and require readback, then one peer read. Active-link applicability
  is an experiment, not a proven fix. Added explicit quiet-error snapshot before
  local UIC controls. No reset/SMC/clock gate/PA_PWRMODE/storage write/retry.
- Local final269tests PASS56.261s; six ACE/SWEET single-file compilesPASS,
  SWEET code/data/relocations unchanged, imports match linked ABI. Exact patch
  reconstruction/fuzz0 matches compiled source. Private evidence and prepared
  source under research/ace-ufs-lpmclock-20261020. Next publish current branch,
  cached/diagnosticfalse CI, accept exact artifact, fresh native+all preflights,
  prepare prior checkpoint from ACTUAL0102, reverify backups, guardedboot_b ONCE,
  then v4 auto-trial/screenshots/independent AEE and inspect real results.
- gh auth status: no authenticated host; existing connector and logged-in Edge
  Actions page available as established fallback; no credentials copied.

## LATEST ACTUAL0102: mode transition fatal; next clock/LPM audit (2026-10-20)

- Actual0102boot_b SHA db68eb004cdfadaceab341d6ccc8f6e7569165f79c5cc1680965d4f52311e663,
  token0b27a6ed9f4f8b25. Controller28899 TERMINALSUCCESS:ADB78.1s, root/B/
  boot/vendorhashes verified, fullrefs/logs/screen, automaticexpectedphysical
  firmwareFastboot return. Screenshot inspected:Androidhome, noXNUdisplayproof.
- Mode11/gears4/4 reads valid. PA_PWRMODESET44 produced UCCS+UPMS plusUICerror:
  complete1,rc00,IS414,HCS50f,UPMCRS5(PWR_FATAL_ERROR),ticks2552859,REFCLK3.
  FaultPA80000010; DL/NL/TL/DME zero. Selectedlinkstill2/host1,PROBE25100081/
  25100001. CorrectlySTOPPED beforepeerread/DMA; mode44 notreadbackverified,
  NOTsuccessfultransition. Do NOTrepeatthisfailedAUTOexperiment blindly.
- IndependentAEE27173 TERMINALSUCCESS55entriesCRC+size; rawringbyteidentical,
  pmsgSHA275497c49caccdf0a878eebba929845928b0885f2535eaf4ada5cfdeeba8906a;
  archive8371d295565efd2aefaebc6473c80d4bb1fb64aa0cd7897ae96ab4fc0a64c9ab.
- ShippingREA reusedf064...9a03 +matchingGhidrasnapshot. Newprobe Evidence
  ev_ca740a0d94258905c100864884be2c26c35e2b80ade31eff87a95d825c841a54 shows
  SMCc2000276/0x80/1/cached16bitUFSversion AFTER ufshcd_pltfrm_init, notproof
  currentPMICstate or a safe guessedversion. Savedpowerfinding+new2.46MBsnapshot
  inpeerauto; REAsessionCLOSED. NoSMC/resetexecuted. Existinglinkstartup evidence
  ev_87b27f...e3cc0 confirms d0a8=0 +clear d0a6bit6 before freshstartup.
- Pinnedfamilyclocksource +actualFDT identify AO112b8000 gatesbits0,1,2,3,4,8;
  PDN112bc000 bits0HCI/1AES; topck10000000 muxCFG0+10 andCFG14+f0. These
  are declarations/source, NOTliveclock observations. UniPro d0a8 was not read
  on inheritedUP path; itsstate unknown. Next0103 shouldremovefailedAUTOpath,
  addreadonlyclock snapshots and qualify/conditionallyclear actualLPM/deepstall
  only withknownsource/UP/ownership/quiet gates, thenonepeerread. Noreset/SMC/
  blindstartup/ignorederrors. Fullstorage/root/display/touch/iOSunachieved.

## CURRENT0102 written; v4 automatic trial LIVE (2026-10-20)

- Writer41139 TERMINALSUCCESS:boot_b64MiB SHA
  db68eb004cdfadaceab341d6ccc8f6e7569165f79c5cc1680965d4f52311e663,
  token0b27a6ed9f4f8b25. Sending1.387s/Writing0.140s/total1.529s; identity/
  B/unlocked/firmwareFastboot/geometry/hash/source/backups gates passed.
  V4controller launchedONCE withrefs+screenshots; do not restart writer or
  controller. Actualmode/peer/NOPresult unknown. No restore/protectedwrites.

## CURRENT0102 CI/preflights accepted; one-time write starting (2026-10-20)

- CI39404829142/job118568113858 TERMINALSUCCESS, cachedBuild178s/UI4m21s,
  1069direct+2preprocessedhits/1miss. Artifact12256875317 ZIP
  63cbffcae3c12a39a9a8f819e5c72637c7d04c9944ae18a8922e2a3a43bd3f08;
  exactprovenance/SHA256SUMS/newlinkedstrings accepted.17540880Bkernel
  SHA16660e19d63dae2b144d8b37c6e27c209529439475734e48b48c3a781115a3b8.
- Preflight59519 TERMINALSUCCESS9native/Centry/4Android/package267tests.
  Fresh64MiBcandidate SHA db68eb004cdfadaceab341d6ccc8f6e7569165f79c5cc1680965d4f52311e663,
  token0b27a6ed9f4f8b25, prioractual0101ff631...49355 bound, newtokenabsent
  inpriorpmsg. Guardedwriter abouttorun onlyboot_b; checkstate/log forresult.
  No0102physicalresult yet. No backuprestore/protected/slot/GPTchanges.
- StaticREAresumed samehashshippingUFS withsavedGHIDRAsnapshot forpotential
  follow-up power/reset diagnosis, nothardware execution; session remainsopen.

## ACTIVE HANDOFF:0102 FASTAUTO experiment CI LIVE (2026-10-20)

- Nextsource0102 tests the AUTO-mode peeraccess hypothesis established by
  actual0101rc08 inFASTmode, not proven applicableMTKquirk. Read localmode/
  TX/RXgears, require11/4/4, onePA_PWRMODESET44; requireUCCS+UPMS(410),rc0,
  HCS.PWR_LOCAL1,clock/ownership stable; readmode44/gearsunchanged,quiet/UP,
  thenonepeerread. Failedtransition/readback stopsbeforepeer/DMA; noretry/
  resets/SMC/gear/lane/storagewrites. Keeps44 on verified transition forNOP.
- Full267hosttests PASS62.542s, actualmethod fault injection forbothcompletion
  bits/error/HCS/timeout/readback/changedclock/state/oneshot. SixACE/SWEET
  compilesPASS, SWEETunchanged, importschecked; exact0102source/fuzz0 matches
  compiledcontroller. Privatepipeline prepared underace-ufs-peerauto-20261020,
  pinned267tests; exactpriorreceipt isactual0101ff631...49355, not0100.
- Publishedremote6f5b94056e71a99d2da93a0013980434af983e0b. DispatchedONCE
  cached/diagnosticfalse ACE13.5DEVELOPMENT, run39404829142/job118568113858
  LIVE. No0102candidate/phonewriteyet. WaitexactCI -> hash/provenance/linked
  accept -> freshnative9/Centry/4Android/package -> guardedboot_bONCE ->v4.
- Actualphone remains0101SHAff631188cd2857a40b009917ff891394d48b8a743e445fd372f221c69ef49355,
  tokenbf5e0eaef20c1c2c, lastphysicalexpectedfirmwareFastboot fromverified
  automaticreturn. Backups/protectedpartitions/GPT unchanged. Goalunfinished.

## LATEST ACTUAL0101: peer communication fails before DMA (2026-10-20)

- Actual0101 boot_b ff631188cd2857a40b009917ff891394d48b8a743e445fd372f221c69ef49355,
  tokenbf5e0eaef20c1c2c. V4controller24538 TERMINALSUCCESS:diagnosticADB76.2s,
  root/B/boot+vendor readback verified, one288Bmatchingreturnrecord, automatic
  expectedfirmwareFastboot returned withoutkeys. Allrefs/logs/screenshot saved.
  Screen visually inspected: Androidhome+USBpurposepicker/FileTransferselected;
  notXNUdisplay/touch/iOS proof. Retain0101, no originalrestore/protectedwrites.
- NEWREALOBSERVATION: stable selectedUP2/host1 before ANDafter peer transaction;
  localmode11/gears4/4,REFCLK3,XOUFS82. SingleDME_PEER_GET attr1561 returned
  complete1/rc08/value0000009a/IS400/HCS10f/ticks2457197. Errorwords allzero.
  rc08 is UIC_CMD_RESULT_PEER_COMM_FAILURE in pinned ufshci.h; returned value
  is invalid onfailure and NOTlane count. No postclock/DMAallocation/queue
  takeover/NOP issued. Thus peeraccess failure can occur before our DMApath;
  this does NOTexclude anotherDMAfault later or prove PHYhardware defective.
- IndependentAEE47116 TERMINALSUCCESS55entriesCRC+size verified; rawpstore
  byteidentical9339B pmsg SHA d791c9675ce68125ef7c365e4490364e94a6007d33de2677424fdff4d0086247;
  archive cbb52d8e03d2d9d28fb10ccba426c4c2a87a3a147cdea0fe872c2617f5612f3d.
  All0101processes/CI nowterminal; no retry/reflash ofconsumedtrial.
- NEXTRESEARCH: pinned ufshcd_dme_get_attr explicitly switches FAST->FASTAUTO
  for UFSHCD_QUIRK_DME_PEER_ACCESS_AUTO_MODE. MTK reference does NOTprove this
  quirk applies to actualAce. Candidate0102 may test one bounded, gated mode
  transition on a fresh boot before any peerread, verify both UCCS+UPMS and
  HCS.PWR_LOCAL plus localmode readback, preserve gears, thenonepeerread/NOP.
  Hypothesis, NOTestablishedfix. No speculativeSMC/PHYreset; iftransitionfaults,
  preserve raw status/error and stop withoutpeer/DMA/retry. Continuefullgoal.

## CURRENT 0101 actually written; automatic trial LIVE (2026-10-20)

- Guardedwriter60294 TERMINALSUCCESS: onlyboot_b64MiB, Sending1.386s,
  Writing0.167s,total1.554s. Installedcandidate SHA
  ff631188cd2857a40b009917ff891394d48b8a743e445fd372f221c69ef49355,
  tokenbf5e0eaef20c1c2c. Finalserial/product/B/unlocked/firmwareFastboot/
  geometry/source/hash/backup gates PASS. No restore/slot/GPT/userdata/
  protectedpartition writes. Actualpeer orNOP result still unknown.
- V4 auto-trial launched once with UFSreference snapshots+screenshots. Follow
  current controller session; never restart consumed writer/controller.
  Must inspect real logs+independentAEE+screen before reporting behavior.

## CURRENT 0101 packaged; guarded one-time write starting (2026-10-20)

- Native/preflight93481 TERMINALSUCCESS:9nativecases,actualCentry,4Android
  fallback paths and package266-host-test gate. Fresh candidate67108864B
  SHA ff631188cd2857a40b009917ff891394d48b8a743e445fd372f221c69ef49355,
  token bf5e0eaef20c1c2c; prior0100 actual9eca...7946 bound in checkpoint.
  Newtoken absent from prior collectedpmsg, retained-reset latch/fallback
  verified.19originalbackups all rehashed. Writer ready for final serial/B/
  geometry/unlocked/firmwareFastboot gates; only boot_b authorized operation.
- This line precedes write; read phone-trial/state.json and flash-candidate.log
  for exact actualresult. Never restart consumed writer/controller. Next v4
  tools/ace-auto-trial.py with private transport and --ufs-reference-snapshots,
  then actualpeer/NOP evidence and independentAEE/screenshot inspection.

## CURRENT 0101 CI accepted; automatic trial preflights finishing (2026-10-20)

- CI39402884633/job118561674824 TERMINALSUCCESS, remote bccbebdea01f637a5ed35098ac692f5c733b527a.
  Cached build212s,1069direct+2preprocessed hits/1miss; total UI5m17s. Real
  source/KDK and compiler restore succeeded; no raw object/kernel shortcuts.
- Artifact12255816802 ZIP SHA a75047c0c1e4ef5e53a3969f858fafbd259c52af61badcfaff73c0c544906c12,
  provenance commit/run/ACE/cached and SHA256SUMS verified. Actual17540800B
  kernel SHA fdb9a11f6eef1fe78ade2dca0739c7afcbde36e89c2084e6402b8d3834a34472.
  Linked new peer strings/entry symbols/cache CIVAC checked. Source reconstructed
  through0101 exactly matches compiled controller, SHA cfb83241163f9affae9b029f1f72a468e204bef68116ba16029f85f61a12c638.
- Native/preflight session93481 LIVE:9cases+actualCentry PASS;4Android fallback
  checks then package/prepare remain in same process, DO NOT restart. No0101
  write yet. 19originalbackups rehashed successfully against original verified
  device-origin manifest; private backup-reverified.json retained. Current
  actual0100/9eca...7946 still retained; no restore/protectedwrites.

## ACTIVE HANDOFF: 0101 one-shot peer diagnostic CI dispatched (2026-10-20)

- User explicitly resumed full true-phone usable-iOS implementation. Goal remains
  unachieved. No new phone write yet; actual0100/hash/token unchanged below.
  Fresh serial-bound Fastboot checks PASS: expected product/B/unlocked and
  is-userspace=no, private initial-fastboot.json under ace-ufs-peer-20261020.
- Source0101 adds one DME_PEER_GET PA_CONNECTEDTXDATALANES(0x1561/op3) on
  actually stable inherited UP, after XOUFS adoption but BEFORE post-link clock
  config, DMA allocation and queue takeover. One-shot guard, bounded existing
  wait, observed status/rc/lane validation, refreshed state after debug mux,
  error snapshots and immediate stop on failure. No peerSET/power-mode change/
  reset/SMC/storagewrite/retry. Successful peer read is NOT NOP/DMA/block proof.
  FAST peer-access quirks may cause rejection; failure alone is NOT dead PHY.
- Reviewed pinned OnePlus ufshcd.c peer read and fetched matching unipro.h into
  ignored research/ace-ufs-peer-20261020 with URL/SHA manifest. Family reference,
  not exact shipping source proof. Existing response poison/OCS05 hardware
  failure remains current established result until new physical logs exist.
- Full host suite266tests PASS (final run log); actual-method fault harness
  covers timeout/rc/stale status/invalid lanes/clock/identity/changed state and
  no second command. Six ACE/SWEET Mach-O compiles PASS; SWEET code/data/relocs
  unchanged, all driver imports present in actual existing linked kernel ABI.
- Remote patch commit bccbebdea01f637a5ed35098ac692f5c733b527a on
  UnrealXu/ios-sweet:codex/ace-initial-platform. UI dispatch ONCE, cached,
  diagnostic_artifacts=false, ACE/13.5/DEVELOPMENT. Run39402884633/job118561674824 in progress;
  follow exact run/Edge3/tab590271818, do NOT repeat dispatch. gh has no auth,
  connector and existing logged-in UI used; no credentials copied.
- Newpipeline scripts syntax checked; must fill exact current run/job IDs,
  accept exact linked kernel/provenance/artifact hash, build fresh token/native
  9cases/C-entry/4Android guards/package266; prepare prior checkpoint from
  actual0100 automatic trial. Then guarded boot_b once and v4 auto-trial with
  references/screenshots, offline inspector + independent AEE. Script paths
  private research/ace-ufs-peer-20261020; NO0101image/phonewrite yet.

## ACTIVE HANDOFF: UniXNU source review; keep Ace mainline (2026-10-20)

- User requested cloning https://github.com/UniXNU/UniXNU and discussing its
  relevance to the final usable-iOS-on-phone goal. This turn is research and
  discussion, NOT authorization to replace the kernel/platform or deploy sheng.
- Cloned full repository into ignored research/UniXNU, clean checkout at
  7b52e7968c76453cdc18b5aa174fc368d5293b91 (main). No upstream scripts run,
  dependencies fetched, code imported, new CI dispatched or device accessed.
  Third-party sources remain out of this repository's git history.
- Read current/earlier handoffs, current actual-ufs-activehandoff-evidence.json,
  UniXNU docs, feeds, NativeUfs production queue/command/root paths and prelink
  design. Current Ace remains candidate0100 boot_b SHA256
  9eca643fcd7604751a10d9668942df6cfdd90c738de3061520e28a9e7ad57946,
  token4eb2d7c3c4dab51a; last verified firmware Fastboot, NOT freshly inspected
  this turn. No phone writes/reboots/restore; backups/protected partitions intact.
- UPSTREAM-REPORTED, not independently reproduced: docs/zh/devices/sheng.md
  says original iPadOS17.7.11 userland reaches SpringBoard/lock/home/Settings
  with touch and CPU rendering. UniXNU-sheng main README support table lists
  display/touch available; Wi-Fi/Bluetooth/camera/GPU/USB/audio/sensors/battery/
  suspend-resume unavailable. Thus valuable userland reference, not demonstrated
  daily-use parity. Live README read through web; docs site fetch failed, use
  the actual cloned docs and pinned GitHub source links for precise evidence.
- CODE OBSERVATIONS: feeds pin XNU10063.141.1/Darwin23.6 vs our8796/Darwin22.
  Main board is sheng SM8550 with UEFI/Mu-Silicium, 4KiB XNU and 1024-byte
  BootArgs command line. Ace already has working native entry/16KiB foundation;
  do not switch page size/BootArgs/OS version blindly or retry fastboot boot.
- NativeUfs is NOT a generic MTK backend: qcom,sm8550-ufshc matching, HC base
  0x01d84000, GCC clocks and apps SMMUv2 base0x15000000/stream0x60, board-
  specific bypass quirk. Native root assumes LUN0; Ace userdata verified LUN2.
  Its hostBringUp also needs genuine NOP before power query/device wake. That
  later wake step is not established as our fix for current OCS05/PA_INIT/DL
  timeout with 512/512 response poison. Do not transplant Qualcomm MMIO/SMMU.
- REUSE CANDIDATES: TransferPoll/RootQueue/RootCommands validation/quarantine,
  RootLayout/RootPublication bounded root windows, NativePrelink Apple kext
  binding, trust cache/AMFI/APFS/IOSurface/display and HID publication methods.
  These require ABI/version/licence review and device-specific backends.
  NativeGeniSpi/Novatek/Adreno hardware paths do not supply MTK/S3910/display
  support. Data is initially a separate RAM seed in upstream; persistent Data
  and reboot survival need separate proof for the user's normal-use objective.
- RECOMMENDED NEXT (proposal, not executed): retain existing Ace automatic trial
  and cached CI; first compare actual reconstructed Ace transport with upstream
  production helpers and shipping MTK initialization/ownership, distinguish
  peer/PHY/clock failures from descriptor/DMA visibility with bounded evidence.
  A next candidate must address a concrete established discrepancy, one fresh
  token and existing automatic readout/return guards; no speculative reset,
  error suppression or blind LINK_STARTUP retry. Gate progress on genuine NOP,
  then LUN2 capacity/read-only GPT, root mount/launchd, actual display+touch,
  then persistent Data and daily-use peripherals. Userland/prelink source study
  can proceed offline alongside storage diagnosis; no wholesale migration now.
- Previous build acceleration and hardware facts below remain authoritative.
  No new build/boot result exists this review; iOS goal remains unachieved.

## ACTIVE HANDOFF: build acceleration COMPLETE; resume genuine UFS fault repair (2026-10-20)

- Latestuserrequest(speedCI/defaultfuturemethod) implemented+published+measured.
  Finalworkflow/helperremotea188ed4605087258c4446368c350ac169710f528, cacheddefault,
  source/KDKcache+strictnativeCCACHE, no__FILE__rewrite/no rawkernel/object/
  generatedheader/fakerootrestore; fullauditmode available, kerneluploadfirst,
  optionaltree/KDKdiagnostics, metrics/provenance preserved. Currentpublished
  forkbranchcodex/ace-initial-platform; do notdispatcholdmainworkflowbyaccident.
- Finalcold#22run39399197726/job118549384099 TERMINALSUCCESS325sBuild,
  419.952sjobspan,1072misses; compatibleKDK/sourcecache restored. Finalwarm#23
  run39400358312/job118553239184 TERMINALSUCCESS172sBuild,222.372sjobspan,
  1070direct+2preprocessedhits/0misses, all1072cacheablecalls hit. Originalfull
  #19Build358.038s/job398.413s. Improvement~52%Build/~44%jobspan. UIworkflow
  total#19=6m50s ->#23=3m50s, notsameaslogspan; queue/changedsourcecanvary.
  Finalsuccessscreenshotprivateci-speed-20261020/final-warm-success.jpg.
- Finalartifact12253403879 ZIP SHA4610609983d1ae2482b9484e5ce42f3c76ac620a43cd1db8a41b7fb2735d72e3;
  source/provenance/SHA256SUMSverified. WarmkernelSHA114d2de54800e18e9a441a4b587171971a4d0601a0ce1ef2419a3d9f23ca9297.
  46non-CTFsections (code/data/layout/zerofill) match BOTH originalfull#19
  kernel58aa194...bd3603 andfinalcold#22kernel32d2f786...c7944c. RawfileSHAs
  DIFFER dueCTFtype metadata; neverclaimbyte-identicalfile/functionalproof.
  Sectionaudit tool+4tests added,6cacheguardtestsPASS/actionlintPASS.
  BenchmarkJSON/timings/artifacts/audits remainignoredresearch; Chineseguide
  docs/KERNEL-BUILD-SPEED.zh-CN.md haslinks/evidence/limits. AGENTSrecordsdefault.
- Currentactualphone remains0100 boot_b9eca643fcd7604751a10d9668942df6cfdd90c738de3061520e28a9e7ad57946,
  token4eb2d7c3c4dab51a, actualroot/hash/vendorBverified; v4automatictrial96423
  TERMINALSUCCESS andAEE90393TERMINALSUCCESS. Newcachedkernelsnotflashed; do
  notreflashidenticalruntimecodejustbecausecacheoptimized. No protected/GPT/
  userdata/slot changes ororiginalrestore. LastverifiedfirmwareFastboot.
- NEXTmainline: genuineNOPstillOCS05/PA_INIT/DLreplaytimeout despite stableUP
  pre/post andadoptedclockconfig. FaultPROBE25100081 vsbefore21100081, clocks3,
  HCS501/IS815, response512poison, requestCRCunchanged. NeeddeeperactualMTK
  PHY/controller/peerownership/transferfault diagnosis fromshippingdriver+new
  boundedreadout, not moreLINKSTARTUPretry/ignoredfaults/claimlinkUP=storage.
  Evidence/facts inpriorhandoff below. FulliOSgoal ACTIVE/unachieved; no new
  codechange/CIrun required for thecompleted speedtask. No liveprocesses/jobs
  remain. Keeprequestedfullgoal/protectedpartitions/backups andrealdeviceproof.

## ACTIVE HANDOFF: first speedup measured; preserve-path correction in validation (2026-10-20)

- Userbuildspeed task: initialcache cold#20run39396136122/job118539230942
  TERMINALSUCCESS, Build402s/step418.4s includingKDKcopy; wholejob481.7s,
  1072misses/0hits, bothcachepostsaved. Warm#21run39397455773/job118543631511
  TERMINALSUCCESS, Build163s/step163.7s, wholejob225.5s;1070direct+2preprocessed
  hits/0misses(100%cacheable), source/KDKrestore17.6s/compilerrestore1.7s/
  sourcecleanup+KDKcopy13.6s includedintotal. Originaluncached#19Build358.0s,
  wholejob398.4s. ThusinitialwarmBuild~54%faster,total~43%faster, not1-2min.
- Downloadinitialcold20(zipSHAe59f7bd3d6b4c445e75e37f50c31e31fd7b21d27c07d581193b31e3be4fdbbfc)
  andwarm21(zipSHA6f109e3736009c7c28d22fe3c8e1cd02bcaeedffdc67f91e79142f06c9912c4f)
  verified. Rawkernels differ, NOTidenticalchecksum! Sectioncomparison shows
  EVERYnon-CTFsection cold/warm byte-identical; __CTFtypeinfo differs. Compared
  toolduncachedbaseline, CCACHE_BASEDIR also rewrote__FILE__strings, causing
  cstring/address-layout changes. Do notmisreportbaselinehashmatch.
- Correctedhelper toCCACHE_BASEDIRempty,preserveoriginalpaths; local17ee4c4,
  remoteworkflowa188ed4605087258c4446368c350ac169710f528. Source/KDKfallback
  prefixallowscompatiblepristine-reset depscrossrecipehash, whilecompilerkey
  stillinvalidates. actionlint/4testsPASS. NewcachedvalidationdispatchedONCE
  inEdge3/tab590271818; needretrieve run/job ID fromsamepage (dispatchobservation
  maytimeout, neverrepeat). NEEDnewartifactruntime-sectionvsuncachedbaseline,
  newwarmperformancecheck ifnecessary; no claimfinalversionvalidationdoneyet.
- MAINLINEactual0100completed: installedboot_b9eca643fcd7604751a10d9668942df6cfdd90c738de3061520e28a9e7ad57946,
  token4eb2d7c3c4dab51a. V4controller96423TERMINALSUCCESS/ADB78.1s/fullrefs/
  screenshot/autoFastbootreturn. AEE90393TERMINALSUCCESS55entriesCRC+size,
  rawpstorebyteidentical11444BpmsgSHA949f31a09179c9357e6eb64c2154749c6199a4325605b585c2a67b0d16e1c75e;
  archive333c2f3e484ddcb2871fbede16c0c489f8edd97ffb9cf88044ee4742f2f2e110.
  Screenshotvisuallyinspected:Androidhome+USBpurposepicker/FileTransferselected.
- ActualUPadoptionworkswithoutfreshLINKSTARTUP; D0A690->9d,D0A13f->1f,
  power11/gears4/4,3quietstates, beforeNOPselectedUP2/host1. NOPstillOCS05/
  HCS501/IS815,PA80000010/DL8000a002; response512A5/requestCRCunchanged.
  FaultPROBE25100081twice (before21100081/21100001), stilllink2/host1. Thus
  UPandlocalpostclockconfig DO NOT fixpeercommunication. No genuineNOP/DMA/
  blockread/rootmount/iOS. Preserveactualfailure fornextPHY/controllerownership
  investigation afterCIoptimization; noreset/SMCguess/protectedwrites/restore.

## ACTIVE HANDOFF: cached-build cold run and actual0100 trial LIVE (2026-10-20)

- Buildspeedbenchmark cold#20run39396136122/job118539230942 stillBuild/in_progress,
  cachepreparestepsPASS. No warmdispatch until terminalpostcache save; need
  compare realhitstats/time/hash against uncached#19kernel58aa194...bd3603.
  No source/workflow changes duringcold/warm pair (cachekey recipehash pinned).
- Mainline259hosttests11361 TERMINALSUCCESS41.715s; fullnewnative9cases/Centry/
  4Androidfallback/package9334 TERMINALSUCCESS. Candidate64MiB
  SHA9eca643fcd7604751a10d9668942df6cfdd90c738de3061520e28a9e7ad57946,
  token4eb2d7c3c4dab51a. Exactguardedwriter79183 TERMINALSUCCESS:
  Sending1.386s/Writing0.147s/total1.534s, onlyboot_b. Targetidentity/B/unlocked/
  geometry/backups/source/verifier hashes passed. No restore/protected/slot/
  GPT/userdata write. Actual0100bootresult unknown until currentlogs.
- V4 controller96423 LIVE with refs/screenshots; do not restart it/writer.
  Waitterminal then inspect-trial.py+independent-aee.py, inspectactualUPadopt/
  postvendorclock/quiet/firstNOP/faultselectedstate. If genuineNOPstillfails,
  don'tclaimfixsuccess or equateUPwithstorage. Bothbuildspeedtask andfulliOS
  mainline continue; no pendinguserpermission/physicalaction currentlyneeded.

## ACTIVE HANDOFF: user-requested build acceleration under live measurement (2026-10-20)

- User asks to speed subsequent builds and adopt improved path permanently.
  Local3e0f306/remote workflowf47c4986daba495b6a1dead32a58cf9818aee613:
  nativeXNU CCACHE interface, explicitstrictconfig/compilercontent, partitioned
  compiler/SDK/machine/config cache keys; source+KDK cache resetsGitpristine
  before patches; nofakeroot/generatedheaders/rawbuild/linkedkernel restore.
  Defaultcached; fullbypassesbothcaches; optionaldiagnostics/fullpreservetree.
  Verifiedkernel uploads before logs/tree/KDKsymbols. Metrics includeBuild
  seconds/rc/ccache counters/provenance. AGENTS/docs/defaultpolicy saved locally
  andpublished. actionlint1.7.7PASS,4cacheguardtestsPASS, diffcheckPASS.
- Coldcache xnu#20 run39396136122/job118539230942 LIVE Build/in_progress after
  restore/preparesteps success. Do notstartwarmuntilthisjobterminalincluding
  postcache save, do notcancel/restart it. Needrealstats/warmrun/samekernelhash
  before claimingacceleration. Privatebenchmarkstate underci-speed-20261020.
- Samekernelbaseline#19 run39394334327/job118533204188 TERMINALSUCCESS;
  original Build358.038s; totaljob~398s fromconsoletimestamps. Artifact12250869047
  ZIP SHA40875644603f9f9584beac30b4cc77e01af76d860b7b5a315d09f54a27e8244f,
  actual17540800Bkernel SHA58aa194aeaa9584d1f713b86d477db9d96f6f7339d81e404f26da58cd8bd3603.
  Needcomparecold/warmkernel withthisbaseline. Kernelpatchesidenticalthrough0100.
- Parallel usefulmainline: baseline19artifactaccepted byactivehandoffacceptor;
  full259hosttests11361 LIVE afterCIcache4tests added (old255 notsilently reused),
  package gateupdated259. Nextwaittests toterminalthenexistingbuild-and-check.py
  freshnative/preflights; no0100phonewriteyet. Actualphone0099 remains9ad90...
  4d096. Allusualidentity/hash/recovery/newtoken guardsandprotectedpartitions
  persist. FulliOSgoalunachieved; do notsubstituteCI speedforhardwareproof.

## ACTIVE HANDOFF: 0100 CI live;255hosttests pass (2026-10-20)

- Localdafb54f, remote60e39d0d231c04b318c8b43fbeed215188fc1de4. DispatchedONCE
  xnu#19 run39394334327/job118533204188, connector confirms Build/in_progress.
  Edge3/tab590271818 retained, private ci-dispatched.jpg/ci-state.json saved
  underresearch/ace-ufs-activehandoff-20261020. InitialCDPobservationtimeout
  wasnotdispatchfailure; samehandle resolved, no duplicate workflow.
- Fullhost81448 TERMINALSUCCESS255tests47.986s. Focusedactualapplied-method
  test98338PASS,6ACE/SWEETcompiles79006PASS, exactsource/patch/ABI unchanged-
  SWEETchecksPASS. SixCI/native/package/guardedtrial/inspector scripts prepared
  for exactnewCI and actual0099priorautomaticloopcheckpoint; ADT copied.
  Acceptance requires newadopt-UP/refusal/post-link/firstNOP strings inlinked
  kernel, retainsoldfresh-link path strings, removesobsoleteoldcomplete-message
  requirement. No0100image yet or phonewrite; actual0099 stays9ad90...4d096.
- NEXT follow exactCIterminal, digest/commit/linkedaccept; newtoken native9cases/
  Centry/4Androidfallback/package, exactguardedwriteonce/v4controllerwithrefs,
  inspect UPhandoff/postlocalclock/quiet/selectedstate/NOPfault+AEE/screenshots.
  Do not assume fixworks because testsPASS or linkUP; needgenuineNOP/blockdata.

## ACTIVE HANDOFF: 0100 active-UP adoption source validated (2026-10-20)

- New0100patch takes actual stable source-selected link state seriously: diagnostic
  returns state only after mux readback/restore, stablelink/host1 snapshots and
  fresh ownership/refclk checks. Board path pins observed HW00360000; unknown/
  unstable/hibernating/lost/config states stop. StableUP skips prelink/startup,
  executes shared fourvendorpostlinkclockops+powerinspection+selectedUP+3quiet
  samples. Supported0/1 retain old singlefresh-start path; rc1 never ignored.
  Before firstNOP rechecks selectedUP, fault capturesvendorstate ifHCE/refclk/
  queueconditions permit. Noreset/SMC/peer/PA_PWRMODESET/storagewrite added.
- Newtests reconstruct exact controller from0090..0100 patches before compiling
  actual methods; active/down/mux/restore/unstable/clock/ownership/UIC/snapshot
  fault cases PASS after fixing mock map equality for zero-valued read keys.
  Compile79006 TERMINALSUCCESS:6ACE/SWEET objects, unchangedSWEETcode/data/
  relocation, importsactualkernelABI. Reconstructedsource byte-identical to
  compiledcontroller. Fullhosttest81448 LIVE; wait exactsession, don'trepeat.
- No0100CI/phonewrite yet. Actualphone remains0099SHA9ad90bb0712018610c288e882fa892b6c53460ed3b55c6e26feefd6f9c44d096,
  expectedFastboot freshlyconfirmed. ActualUPdoesnotprovepeercommunication;
  even ifstartupgatefixed, priorOCS05/PA_INIT failure may persist. Next publish
  exactpatch+fullCI+newnativecases/Centry/fallback/package/guardedtrial, then
  genuineNOP/blockdata/independentAEE evidence. FullgoalstillACTIVE/unachieved.
- User updatedgoal tocontinue deeperrepair when technicalconditions block;
  preservebackups/protectedbootloader/recovery/modem/persist/noGPT, actual
  usableiOS/display/touch/storage/basicoperation remain completioncriteria.

## ACTIVE HANDOFF: 0099 real link UP; repeated startup rejected (2026-10-20)

- CURRENTinstalled0099boot_b64MiB SHA9ad90bb0712018610c288e882fa892b6c53460ed3b55c6e26feefd6f9c44d096,
  token823383298a00dd36. Real root/B/boot/vendor readback verified unchanged.
  Controller82421 TERMINALSUCCESS: ADB78.1s, full logs/refs/screen, one288B
  return-record match, one adb reboot bootloader rc0; physical expectedUSB
  firmwareFastboot/product/B/unlocked confirmed. No keys/restore/slot/GPT/
  userdata/protectedpartition writes. v4 automatic screenshot workflow works.
- Actual state beforeinit HW00360000/major36, selected1/restored1,
  PROBE21100001/21100081 => link2/2,host1/1. Afterinitfailure21100081 twice,
  link2/2,host1/1, selected/restored1. This is actual source-selected vendor
  VS_LINK_UP/VS_HCE_BASE evidence, unlike prior genericHCS inference. Does not
  prove peer/NOP/DMA/storage success. Do not inferSoC=MT6899 from HWmajor36.
- Cold PA80000011/DL80005810/IS4 -> nextallzero/IS4 -> ack -> thirdzero/IS0.
  Localpower11/gears4/4, XOUFS2->82. FourprelinkUICops allrc0; one LINK_STARTUP
  op16stillrc01/IS400/HCS10f/no validUICerrorwords, thenstopbeforeDMA/queue.
  Precise rc01cause remains unproven; do not label invalidattribute or success.
- Independent78406 TERMINALSUCCESS:55AEEentriesCRC+size verified, pstore
  byte-identical9642Bpmsg SHAc8e956837fae61d59839060f4362b9280d15772d4c20c5f181e0dd615b832ea2;
  archiveSHA8eea5e4a6de695a91a7efdd2aaecca6f8542e79385834bca63660d7d7bb1e7c9.
  Screenshot2066750B SHA96d89a9e295467b9123fd59ec0fd0f33104f33810f5b5097c70e270748f9687d
  visually inspected: stockAndroid home+USB-purpose chooser/FileTransfer selected.
  Screen evidence only Android, not XNUdisplay/touch/iOS. Privateactual-evidence
  JSON recordsloopPASS but genuineNOP/DMA/blockread/rootmount/iOS allfalse.
- NEXT concrete source change: respect actually inherited stable UP/idle link
  rather than unconditionally issue fresh-link preconfig/LINK_STARTUP to it.
  Design identity/version/muxrestore/stability/refclk/HCS/error gates, reuse
  platform post-link clock setup only if justified by shippedreference; retain
  fresh-link path for supported down states, no silentignore rc1. Observe actual
  selected vendor state again around firstNOP/fault, and require genuine response
  before disk reads. Do not equate UP with functional storage or promise this
  will fix priorOCS05. FullPHY/controllerreset/peerownership may still be needed.
  Implement/test/compile/completeCI/newtoken/nativeguards/realtrial as usual.
- No liveprocesses remain: CI39391628142,download90525,preflight64432,
  writer87442,controller82421,AEE78406 all TERMINALSUCCESS. GoalACTIVE; this
  turn actualhardwareevidence changesnextaction. No blockers/noiOScompletion.

## ACTIVE HANDOFF: actual 0099 written; v4 trial LIVE (2026-10-20)

- Fresh9nativecases/Centry/4Androidfallback/package session64432 TERMINALSUCCESS.
  Candidate64MiB SHA9ad90bb0712018610c288e882fa892b6c53460ed3b55c6e26feefd6f9c44d096,
  fresh token823383298a00dd36. Guardedwriter87442 TERMINALSUCCESS after exact
  target product/B/unlocked/firmwareFastboot/geometry/hash/backup guards;
  Sending1.388s/Writing0.138s/total1.527s. Onlyboot_b written. No restore,
  protectedpartition/slot/GPT/userdata write. Actual0099startupresult pending.
- v4 automatic controller session82421 LIVE with UFSreferences+best-effort
  Androidscreen evidence. Never restart same consumed writer/controller.
  Wait terminal, inspect-trial.py verifies allcollectedartifacthashes and
  records actual return status separately, then independent-aee.py. If failed
  transport check, preserve failure and freshidentity/token before any separate
  return command; do not call wholeloop successful. No iOS success claim.

## ACTIVE HANDOFF: 0099 CI accepted; fresh preflights LIVE (2026-10-20)

- CI39391628142/job118524297347 TERMINALSUCCESS. Download90525 TERMINALSUCCESS;
  artifact12250172350 ZIPdigest bda9a060d4d80bc9735c0681edc8a472e1e37883276a317216363d12bb6e7011
  matchesexpectedCIcommit5ed77f28a3269b649ee56411b305964398f47573. Acceptor
  verified actual17524352Bkernel SHAebbcff943769a6cb765ccae124544afe2259ceb0edd21d09e21038615cce0f34,
  selected-link diagnostic strings/entrysymbols/cachehelper; not hardwareproof.
- build-and-check.py session64432 LIVE, freshnativebundle built,9nativecases
  running. Wait same session through C-entry/4Androidfallback/package, do not
  restart. Still no0099write; currentactualinstalled0098b0a04...cabd46.
- Fresh expectedFastboot present. Inspector now checks collected-artifact hashes
  and records automatic-loop/separate-return flags independently, so a future
  transport-return failure does not prevent offline evidence inspection or
  masquerade as loop PASS. No currentcontroller running, no originalrestore.

## ACTIVE HANDOFF: 0099 CI LIVE, screenshot workflow committed (2026-10-20)

- Local source8698999; remote0099patch commit5ed77f28a3269b649ee56411b305964398f47573.
  Dispatched ONCE xnu#18 run39391628142/job118524297347; connector confirms
  Build in_progress. No0099image yet, no second dispatch. Edge3/tab590271818
  retained/marked handoff; screenshot ci-dispatched.jpg saved under private
  research/ace-ufs-vendorstate-20261020. ci-state.json pins exactIDs/source.
- 254hosttests session47729 TERMINALSUCCESS35.192s; sixACE/SWEETcompiles23585
  TERMINALSUCCESS; selected-mux actualeffecttestPASS; exactpatchfuzz0PASS.
  Sixnextpipeline scripts prepared/syntaxchecked andADT copied. Newacceptor
  requires selectedlinkstate actuallinkedstrings plus allpreviousentry/cache/
  UFSguards. Packagepins254tests. Priorcheckpoint intentionally accepts actual
  separate-return verified state and preserves originalcontrollerexit1; no
  false automatic-loop claim. Fresh source/hash/token/9native/Centry/4fallback
  still required after CI completes. Do not run writer before those finish.
- CURRENTactualphone boot_b b0a04e4771fc510e4ecde831c29a76d1c14908a3cfc36b4b7cce08c698cabd46,
  lastphysicallyverified expected firmwareFastboot/product/B/unlocked after
  single wirelessreboot; no routine restore or protectedpartition changes.
  FullgoalACTIVE; actualUFS LINK_STARTUP rc01 isestablishedfailure; nochosen
  vendorPROBE evidence yet, noNOP/blockread/rootmount/usableiOSproof.
- NEXT poll exactliveCI to terminal; on success download/verifyartifactdigest,
  accept-kernel.py, build-and-check.py, guarded one-time boot_b writer then v4
  auto-trial --ufs-reference-snapshots. Inspect actual selected/restored PROBE
  fields beforeinit/initfailed plus UIC/fault/AEE/currenttoken; no blindretry.

## ACTIVE HANDOFF: actual 0098 rejected LINK_STARTUP; 0099 source ready (2026-10-20)

- 0098 real boot_b write succeeded, SHA b0a04e4771fc510e4ecde831c29a76d1c14908a3cfc36b4b7cce08c698cabd46,
  token e8cb1b3b1eefb74c. Actual Android root/B-slot/boot/vendor hashes reverified
  over wireless. Original controller77241 TERMINAL EXIT1 after full evidence
  collection: phone absent during return-token observation; no reboot command
  was sent by that controller. Never restart it or mislabel automatic loop PASS.
- Wireless returned, current288Btoken matched; screenshot android-desktop.png
  saved and visually inspected: actual stock Android home. Phone USB later
  enumerated22d9:2765 but only wireless ADB available. Separate recover-return.py
  session33853 TERMINALSUCCESS: fresh serial/currentrecord verified, one wireless
  adb reboot bootloader rc0, then expected USB firmware Fastboot/product/B/
  unlocked physically verified. State diagnostics-collected-separate-return-
  fastboot-ready, originalfailure preserved. No new write/restore/slot change.
- Actual new result: cold PA80000010 clears in3samples; power11/gears4/4,
  XOUFS2->82 verified. LocalUIC SETD0A8=0/SET155E=0/GETD0A6=90/SETD0A6=90
  all rc0/IS400. Single LINK_STARTUP op16 returns rc01/IS400/HCS10f; no valid
  PA/DL/NL/TL/DME error bits, no retry or transfer queue writes. No genuine
  NOP/DMA/blockread/rootmount/usableiOS. Need actual selected vendor link state,
  not a guess that restarting an already-established link is supported.
- Independent AEE61525 TERMINALSUCCESS,55entriesCRC/size checked, pstore ring
  byte-identical to9341B pmsg SHA34c1094a1a1dba9dc472a443f761c3a891112d3cf001e4fe0f48ccfeb13f1ade.
  ArchiveSHA5610f3bd40a7e7fb8d1c4681135bf0debfc138dd3a0014ceaf84b422e2c23bb4.
  Evidence under research/ace-ufs-linkstart-20261020/phone-trial; partial evidence
  file does not assert successful automatic return. Screen screenshot SHA
  12de5186a2c1d86c458b8a2b589552d8def0c8abae6b922ea2ab1518e4ceab1f.
- Added0099 diagnostic source: readHW2240; choose source-matched debugmux
  (major>=36:820820+B0..B3; otherwise20); verifyselection, twoPROBE samples,
  restoreeveryselector, logselected/restored/link/host beforeinit andonfailure.
  Invalidversion/unready/refclock guards. No resets/SMC/new UIC/storage writes.
  Exactpatchfuzz0/actualmethodeffecttestPASS; sixACE/SWEETcompiles23585
  TERMINALSUCCESS, SWEETcode/data/relocations unchanged, importsactualABI PASS.
  NOT yet completeCI-built/packaged/flashed; next publish0099+CI, accept actual
  linked code, fresh native9cases/Centry/4Androidfallback, newtoken/guardedtrial.
- User requests screenshots automatically: AGENTS updated; controller v4 saves
  best-effort validated PNG and hash after identity/hash checks; 16controller
  testsPASS. Screenshots prove only Android visible state; never claim early
  XNU/Fastboot screen capture through unavailable adbd. Full goal remains unmet.

## ACTIVE HANDOFF: 0098 flashed; automatic trial LIVE (2026-10-20)

- USB returned: expected exact Fastboot device enumerated as MediaTek 0e8d:201c.
  Guarded writer 95718 TERMINAL SUCCESS after candidate/backup/source/verifier
  hashes and product/B/unlocked/firmware-Fastboot/geometry checks. Only boot_b
  written, 64MiB SHA b0a04e4771fc510e4ecde831c29a76d1c14908a3cfc36b4b7cce08c698cabd46.
  Sending1.389s/Writing0.137s/total1.528s. Trial token e8cb1b3b1eefb74c.
- Automatic controller session 77241 LIVE with --ufs-reference-snapshots.
  Do not restart writer/controller. Wait same session to terminal, then inspect
  trial and independent AEE only on success/expected phase. No original restore,
  protected partition/slot/GPT/userdata write. USB absence blocker has cleared;
  full iOS goal still unachieved, new link initialization hardware result pending.

## Latest screen confirmation (2026-10-20)

- User confirms screen is Fastboot. Fresh host checks still show no expected
  Fastboot/ADB transport and no phone in lsusb or USB sysfs. All enumerated
  USB devices/root hubs have authorized=1; no evidence of host USB authorization
  blocking an enumerated phone. User screen report and host absence are separate
  observations; cable/port/phone connector cause remains unproven.
- Next external action: reseat/change host port and a known data-capable cable
  while leaving phone in Fastboot. Do not ask to re-enter Fastboot unnecessarily,
  reset unrelated host USB devices, or start a writer waiting for any serial.
  No candidate write or reboot performed; 0098 remains unconsumed.

## Latest user reconnect attempt (2026-10-20)

- User reports USB reconnected and requests continuation. Fresh exact serial
  checks still find neither expected Fastboot nor USB ADB. Full lsusb inventory
  contains only root hubs/webcam/Bluetooth/mouse, no phone; adb devices,
  adb mdns services and fastboot devices all empty with rc0. Last five minutes
  of readable kernel journal contain no USB event. These observations do not
  establish whether the cause is phone mode, cable, connector or host port.
- Asked current phone screen through async input; keep direct data cable
  connected. No writer/controller invoked, no write or reboot performed.
  Candidate 0098 and its unconsumed trial remain unchanged. Resume fresh
  exact identity checks once phone enumerates; do not infer connection merely
  from physical cable insertion or reuse old Fastboot verification.

## ACTIVE HANDOFF: device transport blocked (2026-10-20)

- Latest goal continuation independently checked adb devices, adb mdns services,
  fastboot devices and phone-vendor USB entries: all zero, all commands returned
  successfully. User confirmed USB intentionally disconnected; no current
  wireless endpoint or live wireless ADB transport is available.
- Same missing-device-transport blocker has persisted across at least three
  consecutive goal turns, including the wireless alternative check. Previous
  turn yielded no physical progress or live-process wait; recording the limit
  did not advance kernel bring-up. No remaining independent candidate work is
  justified before the prepared 0098 hardware result. Goal marked BLOCKED,
  pending restored USB access (or an actual Android wireless endpoint for
  diagnostic-only access). Do not invent an ongoing CI/controller process.
- Candidate 0098 remains write-authorized-awaiting-final-bootloader-checks;
  partition_writes_started is empty. No new write/reboot/recovery performed.
  Full iOS goal remains unachieved: no real NOP/block read/root mount or usable
  iOS verification. Preserve candidate, backups and existing protected partitions.
- After user restores USB, revalidate exact phone identity and run the prepared
  guarded writer once, then the automatic trial controller and current-token
  evidence inspection as detailed below. No speculative new kernel/repeated
  unchanged host tests, consumed-controller restart or routine backup restore.

## Latest transport clarification (2026-10-20)

- User intentionally unplugged USB and asks whether wireless ADB can continue.
  Fresh adb devices and adb mdns services both empty; private transport JSON
  contains only the USB identity, no saved wireless endpoint. Current phone
  screen unknown. No 0098 write or reboot performed.
- Wireless ADB may support diagnostics while Android/adbd/Wi-Fi are running;
  it does not establish wireless firmware Fastboot or a recovery connection
  when the experimental kernel hangs. The current guarded boot_b writer and
  automatic return-to-Fastboot workflow still require verified USB transport.
  Do not replace this with an unverified root dd write without recovery access.
- Candidate 0098 remains fully prepared and unconsumed. Next: restore USB
  for the actual trial, or obtain current Android wireless endpoint for
  read-only diagnostics; do not claim that either connection currently exists.

## ACTIVE HANDOFF:0098 host-ready, waitingphoneUSB; onlineauditcomplete (2026-10-20)

- Actualnewcandidate64MiB SHAb0a04e4771fc510e4ecde831c29a76d1c14908a3cfc36b4b7cce08c698cabd46, tokene8cb1b3b1eefb74c.
  Native77594624B SHA0837c7152d3a86225568060948303560992588ecc7b45ddd95422502c59438b3. FullCI39385735286/
  job118505018971SUCCESS, artifact12248060422/source691fe9e... validated;
  fresh9nativecases/Centry/4AndroidfallbackguardsPASS. Process74013TERMINAL
  SUCCESS, guardedwriterprepared inphone-trial, phasewrite-authorized-awaiting-
  final-bootloader-checks/partition_writes_startedEMPTY. NO0098write/reboot.
- CurrentphoneUSB/ADB/FastbootABSENT ontwocomprehensivechecks+finalfreshcheck.
  Askeduserreplugandphonescreenviaasync; responsepending. LastKNOWNinstalled
  adb46f96d93694a8cda7f3688cf23d7c3e1eedbfa1e803abecf82e8e52bfed44,
  lastverifiedFWFastbootfromprevioussuccessfultrial, currentphysicalscreenUNKNOWN.
  DoNOTequateoldstatewithcurrentlyconnectedphone. Neverinvoke writerwithout
  fresh exactidentity/product/B/unlocked/is-userspace=no checks.
- UserrequestedwebresearchDONE: docs/ACE-UFS-RELATED-FIXES.zh-CN.md925d6d3
  compares5primaryreferences/applicability. MTKPA_InitadaptfixMT6899+NOTblindly
  applicable; PWM/AH8/PMrecoveryconfirmstate/sequencechecks, notsameAce/iOScase.
  ActualVS_LINK_UP(debugselector+hardwareversion) isnextquestionIFcurrent
  oneLINKSTARTUPstillfails; don'tmodifytestedcandidatejusttospeculate.
- NEXTifconnectionreturns: freshguardedwriteronce, v3auto-controllerwithrefs,
  inspectcurrenttoken/initop/oneLINKSTARTUP/threepostsamples/firstNOP/block
  data vsindependentAndroidrefs +allAEEentriesCRC. DoNOTrestartconsumedwriter/
  controller, no routinebackuprestore/protected/slot/GPT/userdatawrites.
- GoalACTIVE; onlineresearch/doc+acceptedCI+hostcandidatecompletedprogress.
  PhysicalIOnewblockerfirstgoalturn, notthree-consecutiveblockedcondition.
  StillNOgenuineNOP/DMAroundtrip/XNUdiskread/rootmount/usableiOSproof.
  Preservefullgoal andRAMdiagnosticfallback prerequisitebeforeuserdata writes.

## CURRENT0098 CI accepted; native74013 LIVE; phoneUSB absent (2026-10-20)

- ExactCI39385735286/job118505018971 TERMINALSUCCESS; artifact12248060422,
  source691fe9e95467eb72bc12e6320b832ed1f6d1d879, ZIP SHA
  f1f5ec350349f582a086392b3d2c6b4c894ccc585f9878442991fedb05bf452c.
  Actualkernel17524216B SHA3db12dcc10dc867f701fe7712f1946448fe4b0c4d4079fbe9120e8793ad25450;
  newinit/UIC/linkstartstrings plusentrysymbols/cacheABI checked.
- build-and-check.py74013 LIVE, no0098write. DoNOTrestartwhilelive. NEXT
  waitterminal/preparedconcretecandidate. PhonewaslastverifiedFWFastboot,
  installedadb46...fed44; NOWtwoindependentchecks noFastboot/ADB/phoneUSB
  vendor onbus. CurrentphonescreenUNKNOWN. Askeduserreplug/describe viaasync;
  continuehostwork, neverinvoke writeruntilfreshdeviceidentity passes.
- Useronlinequery answeredwithmaintainerprimarypatches+applicabilitydoc
  docs/ACE-UFS-RELATED-FIXES.zh-CN.md (925d6d3). NoneprovesameAce/iOSsuccess.
  NeedfutureactualVS_LINK_UPifthisone-linkstartstillfails. GoalACTIVE,
  notblockedauditthreshold (newconnectionlossfirstturn), noiOSproof.

## User-requested online related-fix audit (2026-10-20)

- Readmaintaineroriginalpatches andkernelprimarysource; saved/committed
  docs/ACE-UFS-RELATED-FIXES.zh-CN.md (925d6d3), withlinks/applicability.
  FoundMTKPA_Init/adaptation/PWM/AH8/resumerecoverycases; didNOTverifyany
  sameAce+sameXNUlog+usableiOSsuccesscase. Do notclaimoneexists.
- PA_Initno-adaptpatchgateisIP_MT6899+, donotblindlyapplytoMT6895.
  PWMswitchfixhonorsrequestedmode/avoidsinvalidHSadaptation/FASTAUTOrouting;
  currentXNUdoesnotyetsetPA_PWRMODE, so notcurrentprovenfix. AH8patchrequires
  realVS_LINK_UP+idlechecks, notAHIT0alone. This addsconcretenextquestion if
  0098stillfails: verifyvendorlinkstateusingmatchingHWdebugselector, not
  generichostreadyonly. Keepcurrentoneshotkerneltestbeforescopechanges.
- PMcallbackreturn0inrecoverypatchisLinuxPMcontractworkaround, NOTproof
  hardwareworks; keepNOP/blockdata successcriteria. CurrentCI39385735286
  verifiedlive, BuildnowSUCCESS/entryverificationin_progress. No0098writeyet.
  GoalACTIVE; substantiveonlineevidence/applicabilityprogress.

## ACTIVE HANDOFF:0098 single-link-startup CI live (2026-10-20)

- Localab4103b /remote691fe9e95467eb72bc12e6320b832ed1f6d1d879.
  DispatchedONCE xnu#17 run39385735286/job118505018971; connector confirms
  liveBuild/in_progress. NO0098imagewritten. Edge3/tab590271818 retainedforCI.
  Privateace-ufs-linkstart-20261020/ci-state.json andci-dispatched.jpg pinsIDs.
- Sixofflinepipeline scripts prepared/syntaxchecked/ADTcopied. Linkedaccept
  requiresnewinitbegin/UIC/complete/3link-startsamples +allpreviousXOUFS/
  power/cold/fault/entry/cachechecks. Expectedpreviousactualinstalledadb46f...
  fed44/priortrialace-ufs-xoufs-20261020. Package requiresNEW251testsPASS
  38.596s, process88670TERMINALSUCCESS; sixkernelcompiles/exactpatchPASS,
  actualnewmethods66mockUICcasesPASS. Not physicalproof ofnewinitsequence.
- NEXTpollsameexactCItoTERMINAL; onSUCCESS verifyZIPdigest/sourceSHA/actual
  linkedstrings/symbols/cacheABI; accept-kernel.py thenbuild-and-check.py
  fresh9cases/Centry/4fallback/package. Reviewguardedwriter/oneboot_bwrite/
  v3auto-controllerwithAndroidrefs. Inspect everyinitop attr/sent/rc/value/
  status andoneLINKSTARTUPresult, threepoststartsnapshots/newPApower-gears/
  firstNOPresponse/fault. No blindretries/SMC/HCEtoggle/peer/PA_PWRMODESET.
  LocalvendorSETsareexplicitnewscope ofthislinkinitialization, notreadonly.
- Currentphoneboot_badb46f96d93694a8cda7f3688cf23d7c3e1eedbfa1e803abecf82e8e52bfed44,
  actualrootreadback+vendorunchanged, firmwareFastboot/B/unlocked/is-userspace=no
  afterv3trial21194TERMINALSUCCESS/ADB78.1s/one288Brecordmatch/onerebootrc0.
  XOUFS2->82physicallyverified butNOPstillOCS05/PA_INIT/replaytimeout: bit
  aloneFAILED tofixlink. No keys/reflash/controllerrestart/restore/protectedwrites.
- Processes75343/81922/60621/21194/94016/57688/88670 allTERMINALSUCCESS.
  GoalACTIVE: realhardware+falsifiedhypothesis+sourceprogress thisturn;
  notblocked/complete. StillNOgenuineNOP/DMAroundtrip/XNUdiskread/rootmount/
  usableiOSproof. Preservefullgoal andRAMdiagnosticfallback prerequisite
  beforeuserdata overwrite. Keeporiginalbackups/protectedpartitions/GPT.

## LATEST ACTUAL0097: XOUFSbit adopted but NOPfailure unchanged (2026-10-20)

- CURRENTinstalledboot_badb46f96d93694a8cda7f3688cf23d7c3e1eedbfa1e803abecf82e8e52bfed44,
  token8e4c1c90d806e98d; actualrootreadback+unchangedvendorreceiptverified.
  NativeSHA40673faa05e8ccb8d50929a9189b2ba454abab8b70f740048ce776a2bbe907cb. v3controller21194TERMINALSUCCESS,
  ADB78.1s/fullreadout/FWFastboot/B/unlocked/is-userspace=no. One288Brecord
  readmatch/rebootrc0; no keys/controllerrestart/restore/protectedwrites.
- ActualXOUFS2->82 exactreadback+quietUIC/readyHCS verified. REFCLK3/HS-G4
  localGETs stillsuccessful. FirstNOP stillOCS05/HCS501/RSR0/PA80000010/
  DL8000a002/IS815, elapsed2586708ticks; response512A5 andrequestCRCunchanged.
  Thus settingthatbitalone DIDNOTrepaircommunication. NOgenuineNOP/DMA/
  diskread/rootmount. Preservefailedhypothesis, donotlabelbitadoptionsuccess
  storage success. Currentlogs actual-ufs-xoufs-evidence.json private.
- Actualpmsg9538B SHA56c52061023bfe041fe3873db46040c6a877e07bb71aeddbaecec1d42cf79bd3;
  AEE94016TERMINALSUCCESS all55entriesCRC+size/rawpstorebyteidentical;
  archive5f6c6b6a3d76b03dce03475dcc12ffd2d2d6ff606c55cffdad22cef3ad77bf6f,
  recorde3f26e85acb8f87011b11e9fe7b6d1c9fc0ed9196a78e3fb724feb6260945d6a.
- New0098implementsnonsecurelocalMTKpre/postlinksequence frompinnedprimary
  sourceandpreviousshippingREA: SETD0A8=0/155E=0, GET/SETD0A6clear40,
  ONE LINK_STARTUP16, sample/read-clearknownPHY/DLthree times/quietness,
  GET/SETD0A6orD +D0A1clear20, thenrepeat3localPApower/gearreads. EveryUIC
  whitelist/ready/IS/clock/rc/timeoutguarded; no retry/HCEtoggle/SMC/peer/
  PA_PWRMODESET/storagewrites. ThisisNOTfullPHY/controllerresetinitialization;
  outcomeonphoneUNKNOWN. Onlyafterallthis canfirstDMA/NOPhappen.
- SixACE/SWEETcompilesPASS/unchangedSWEET/allimportsactualkernel/exactpatch
  fuzz0PASS. Actualnewmethods mockUIC66caseeffecttestPASS0.944s; nineUICops,
  oneLINKSTARTUPmax, faulteverypositionstops. Fullhosttests88670LIVE; don't
  restart. Privateace-ufs-linkstart-20261020. NEXTcommit/publish0098/fullCIonce,
  freshallpreflights/oneguardedboot_b/v3trial. GoalACTIVE/noiOSproof.

## LATEST0097 WRITTEN; automaticphysicaltrial21194 LIVE (2026-10-20)

- Writer60621 TERMINAL SUCCESS, boot_b64MiB SHA
  adb46f96d93694a8cda7f3688cf23d7c3e1eedbfa1e803abecf82e8e52bfed44,
  token8e4c1c90d806e98d. Sending1.389/Writing0.151/total1.542s. CURRENTimage
  thiscandidate, notolder13508a. No restore/protected/slot/GPT/userdatawrites.
- Native77594624B SHA40673faa05e8ccb8d50929a9189b2ba454abab8b70f740048ce776a2bbe907cb, exactCI39383499165/
  job118497812273/remote31c063...SUCCESS; allfresh9native/Centry/4fallback
  PASS and250hosttestsPASS. Guardedknownphone/B/backup/geometrychecksPASS.
- v3auto-controller21194 LIVE withAndroidreferences; doNOTrestart consumed
  controller/writer. NEXTwaitterminal/readstate, runinspect-trial.py and
  independent-aee.py AFTERfullreadout+FWFastboot. Inspectvendorbefore/after/
  postquietness andfirstNOPresponse/fault. NewhardwareoutcomeUNKNOWN.
  GoalACTIVE/fulliOSnormaluseunproven.

## CURRENT0097 fullCI SUCCESS; freshnative81922 LIVE (2026-10-20)

- CI39383499165/job118497812273 TERMINAL SUCCESS, artifact12246399025
  source31c063f1a8505c8b73a7a598e40cde07d0f0b934, ZIP SHA
  a3066300c067e9db8d9ef8251152d488674dbe395d557de1f771f1514bbc50b7.
- Actualkernel17524040B SHAb781980b9c50c8843a415aedce56997d5cd96ffdd64486af237fe6a401c9ea8e;
  newXOUFSbefore/after/adopt/poststate +previousstrings/symbols/cacheABIchecked.
- build-and-check.py81922 LIVE freshnative/9cases/Centry/4fallback/package.
  DoNOTrestart. NEXTwaitterminal/reviewconcretecandidate+guardedwriter/one
  boot_bwrite/v3controller+Androidrefs. Currentinstalled13508a...79128 still
  authoritative; no0097writeyet. GoalACTIVE/noiOScompletionproof.

## ACTIVE HANDOFF:0097 isolatedXOUFS experiment CI live (2026-10-20)

- Local265db93 /remote31c063f1a8505c8b73a7a598e40cde07d0f0b934.
  DispatchedONCE xnu#16 run39383499165/job118497812273; connector confirms
  liveBuild/in_progress. No0097imagewritten. Edge3/tab590271818 retainedforCI.
  Privateace-ufs-xoufs-20261020/ci-state.json andci-dispatched.jpg pinsIDs.
- Sixofflinepipeline scripts prepared/syntaxchecked/ADTcopied. Kernelaccept
  requiresnewXOUFSbefore/after/adopt/post-snapshot plusallpreviousstrings/
  entrysymbols/cacheABI. Expectedpreviousinstalled13508a...79128; priortrial
  ace-ufs-linkpower-20261020. Package requiresNEW250testsPASS34.186s, process
  87958TERMINALSUCCESS. Kernel6compiles/exactpatch/21effectcasesPASS; earlier
  linkpower24effectcasesPASS. No hardwareproof forthisnewvendorbit yet.
- NEXTpollsameexactCItoTERMINAL; onSUCCESS verifyactualZIPdigest/sourceSHA,
  linkedstrings/symbols; accept-kernel.py thenbuild-and-check.py freshnative/
  9cases/Centry/4fallback/package. Reviewguardedwriter, oneboot_bwrite then
  v3auto-controller+Androidrefs. Inspect XOUFS2->82/readback/quietpoststate and
  actualfirstNOPresponse ornewfault. PRE-HCEshippingcallback!=provenlivehost
  equivalence: doNOTcallthisprovenrepairuntiltruephone. NoSMC/reset/HCEtoggle/
  PA_PWRMODESET orbulkqueuechanges inthisexperiment.
- Currentphone13508a83be1f5faa8dd6f1ca5092e9c2baa576b27a1c8703e2f60ad6f1879128
  rootreadbackverified+vendorunchanged; firmwareFastboot/B/unlocked/is-userspace=no
  afterfullv3automatictrial53090TERMINALSUCCESS; ADB76.1s, oneexact288Btoken
  observationmatch, onerebootrc0. No keys/controllerrestart/restore/protectedwrites.
- Processes20678/33395/43010/53090/48860/74921/87958 allTERMINALSUCCESS;
  REAsessionexportedandclosed. GoalACTIVE; thisturnactualhardware/evidence/
  sourceprogress, notblocked orcompletion. StillNOgenuineNOP/DMAroundtrip/
  XNUdiskread/rootmount/iOSuserspace/display/touchnormaluseproof. Keepfullgoal
  anddata-independentRAMdiagnostic prerequisite beforeuserdata overwrites.

## LATEST ACTUAL0096 +next0097 vendor-control experiment (2026-10-20)

- Currentinstalled13508a83be1f5faa8dd6f1ca5092e9c2baa576b27a1c8703e2f60ad6f1879128,
  token8efbe8908f61d459, actualrootreadback+unchangedvendorverified. NativeSHA
  47e2ae77c715457767813cf094b743cc2b6ac4a5b286781d58e21b538f0d555c. v3controller53090 TERMINAL SUCCESS, ADB76.1s,
  exact288Breturnrecordmatched firstread; onereboot rc0; FWFastboot/B/unlocked/
  is-userspace=no verified. No manualkeys/restart/restore/protectedwrites.
- ActualREFCLK3/XOUFS2, localDME_GET1571->11/1568->4/1583->4 allrc0/IS400/
  HCS10f, elapsed45/41/44ticks. Thus localUICengineworks/refclkreqackon/HS-G4;
  no proofpeerlinkcommunicates. NOPthenOCS05/HCS501/RSR0, elapsed2586692ticks,
  requestCRCunchanged190a55ad, response512A5, PA80000010/DL8000a002/IS815.
  REFCLK3/XOUFS2 unchangedafterfault. NOgenuineNOP/DMAroundtrip/diskread.
- Actualpmsg9228B SHA645fcaaf5190aeb02e89d176787e72e38847e1e027546ef99e841dbd4035a55a;
  AEE48860TERMINALSUCCESS all55entriesCRC+lengthverified/rawpstoreidentical,
  archive3f697233d11cca8585c3eacb71f02a258eeeab8e24334577375692a56aba3889.
  RecordSHA438f5c376b09a49582d66116173d984d365beca61c6417c05457dfab5c71148a.
  Privateactual-ufs-linkpower-evidence.json andAEE evidence.
- REAshippedmodule HCE-enable ev_eda8e5ca0ce393e066377ee9f3ead034ec81fcba6075616b2833ca7d3f2ef816
  confirmsMMIO+140 OR80 inPRE-HCE callback; corroboratedpinnedprimarysource.
  FullREA evidence/snapshot exportedunderace-ufs-linkpower andsessionclosed.
  ThisdoesNOTprovecurrentOCSrootcause, norproveactive-hostadoptionequivalence.
- New0097 isolatedadoption: AFTERexistingcold/clock/3GETgates, requireidle/
  IS0/REFCLK3/XOUFSexact2or82; atmostonewrite140=82; settle1ms, exactreadback/
  host/clock/quietUICrecheck beforeDMA/NOP. Unknownstate/faultrefuses. NoSMC/
  reset/HCEtoggle/DMESET/queuechanges/storagewrites. Its effectonphoneUNPROVEN.
- SixACE/SWEETcompilesPASS/unchangedSWEET/allimportsactualkernel; exactpatch
  fuzz0PASS. Newactual-methodmockMMIO21caseeffecttestPASS0.697s. Fullhosttests
  87958LIVE (doNOTrestart). Privateace-ufs-xoufs-20261020. NEXTcommit/publish0097/
  fullCIonce/freshallpreflights/oneguardedboot_b/v3physicaltrial. GoalACTIVE.

## LATEST0096 WRITTEN; v3 physicaltrial53090 LIVE (2026-10-20)

- Writer43010 TERMINAL SUCCESS, onlyboot_b64MiB SHA
  13508a83be1f5faa8dd6f1ca5092e9c2baa576b27a1c8703e2f60ad6f1879128,
  token8efbe8908f61d459. Sending1.387/Writing0.147/total1.536s. CURRENTimage
  nowthiscandidate, notolder299251. No protected/slot/GPT/userdatawrites/restore.
- Native77594624B SHA47e2ae77c715457767813cf094b743cc2b6ac4a5b286781d58e21b538f0d555c; fresh9cases/Centry/4fallback
  PASS; actual248hostbaseline+new24-caseMMIOeffecttestPASS. FullCI39381648050
  job118491886527SUCCESS; remote2e88ac8b9582e21a1ddcf5a7f3ab512deb776917.
- tools/ace-auto-trial.py53090 LIVE, v3record-observations/refreshedidentity,
  --ufs-reference-snapshots. DoNOTrestartwriter/controller. NEXTwaitexact53090
  terminal; inspectstate; theninspect-trial.py+independent-aee.py onlyafter
  fullreadoutandFWFastboot. Read actualREFCLKandPApower/gears BEFORE NOP.
  No resultsfromthiscandidateyet. GoalACTIVE/noiOSorrootmountproof.

## CURRENT0096 CI SUCCESS; freshnative33395 LIVE (2026-10-20)

- CI39381648050/job118491886527 TERMINAL SUCCESS. Kernelartifact12246076128
  source2e88ac8b9582e21a1ddcf5a7f3ab512deb776917, ZIP SHA
  7c57c366114c52e6b132ab04e2cd8ed0ed6d287dd82701d8a8454c6a5815101b.
- Actualkernel17523976B SHAeb7f19a1aecb93819baa1c4d374849eaafe2a90849339e0cdf356c298273e68b;
  newREFCLK/DMEGET/fault/coldstrings+symbols/cachehelperABI verified.
- build-and-check.py33395 LIVE (newnative/9cases/Centry/4fallback/package).
  DoNOTrestart. NEXTwaitterminal/reviewmanifest+guardedwriter/oneboot_bwrite/
  v3controller withAndroidrefs. Currentinstalled299251...d17e stillauthoritative;
  no0096write yet. GoalACTIVE; allfulliOSrequirementsremainunproven.

## Additional0096 effect verification while sameCI builds (2026-10-20)

- Newtest_ace_ufs_linkpower.py extracts actualpatchedinspect_link_power method,
  compileswithmockMMIO andruns24success/refusal cases. PASS1unittest0.736s.
  All3GETpositions faulttested(timeout/ISfatal/nonzerorc/hostlost/refclklost),
  initialclock0/1/2 emitsNOwrites; pending/unknownstatus/hostbusy emitsNOGET.
  Enforcesnoqueue/powerSET/resetwrites. ThisisHOSTeffectproofonly, notdevice
  behavior. Private mmio-effect-test.json pinsactualtest+patchhash.
- Existing248testbaseline remainsactualfullPASS; newfocusedtest isadditional,
  notclaim ofnewfull249run. CI39381648050/job118491886527 stilllive Build;
  no restart/newdispatch/imagewrite. GoalACTIVE, previoushardwareprogress.

## ACTIVE HANDOFF:0096 exact CI live; currentphone safelyFastboot (2026-10-20)

- Local6ac52aa /remote2e88ac8b9582e21a1ddcf5a7f3ab512deb776917.
  DispatchedONCE xnu#15 run39381648050/job118491886527; connector confirms
  Buildin_progress. NO0096imagewritten. BrowserEdge3/tab590271818 retained.
  Privateace-ufs-linkpower-20261020/ci-state.json andci-dispatched.jpg.
- Sixofflinecandidatepipeline scriptsprepared/syntaxchecked+ADTcopied. Accept
  actualnewREFCLK/DMEGET/clockrefusal/completionstrings andfault/cold/entry/cache
  checks. Source/run/job exactpinned; previousactualinstalled299251...d17e,
  priortrialace-ufs-commandfault-20261020. Package nowrequiresNEW248hosttests,
  allPASS31.926s (process77878TERMINALSUCCESS), notinheritedlog. Sixkernel
  compiles/exactpatchPASS. Fixedv3controller14focusedtestsPASS; fullnextphone
  integrationnotyetverified, priorcontrollererrortruthfullypreservedbelow.
- NEXTpollsameCItoTERMINAL, verifyactualZIPdigest/sourceSHA/linkedsymbols;
  accept-kernel.py thenbuild-and-check.py NEWnative9cases/Centry/4fallback.
  Reviewguardedwriter, oneboot_bwrite, newv3controller withreferences. Inspect
  REFCLKandlocalPA_PWRMODE/TXGEAR/RXGEAR BEFOREfirstNOP, determinewhether
  failurealreadyexistsbeforetransfer. DoNOTblindSMC/reset/SET/linkstartup
  noraccept0x400completionwithoutresult/status/hostchecks.
- Currentphoneinstalled299251071d21fe74c15cae240d6e6ffeda4df11ad5268821cab4c948acd6d17e,
  exactrootreadback+vendorunchangedreceipt retained, firmwareFastboot/B/unlocked/
  is-userspace=no afterprivate18820completedreturn. Original33972EXIT1 was
  pre-returnrecordmismatch afteralllogs; recoveredviafreshidentity/exactrecord,
  no keys/reflash/controllerrestart/originalrestore. No protectedwrites.
- Processes74043/7601/46130/18820/56860/17975/77878TERMINALSUCCESS;
  33972TERMINALEXIT1 preserved. REAsessionexportedandclosed. GoalACTIVE;
  thisturnrealhardware+source/evidenceprogress, notblocked/complete. Stillno
  XNUdiskread/rootmount/usableiOSproof. Preservefullgoal andRAMdiagnostic
  fallback prerequisite beforeuserdata overwrite.

## NEXTSOURCE0096: bounded local link-power reads before first NOP (2026-10-20)

- New0096patch observesMTKREFCLK(+144)/XOUFS(+140) beforetransfer andonfault.
  IfREFCLKrequest/acknotbothon: refusewithoutUIC/queuewrites. Withclockon,
  disableUFSIE forpolling then exactly3localDME_GET attrs PA_PWRMODE1571,
  PA_TXGEAR1568, PA_RXGEAR1583, loggingactualvalue/rc/IS/HCS/ticks/REFCLK.
  Onlyreadyidle/IS0 andsuccessful0x400completion allowed; unknownstatus/
  result/changedhost/refclktimeout refusesbeforeDMA/NOP. NoDME_SET/peerGET/
  LINK_STARTUP/reset/SMC/storagewrites. Thisisdiagnosis, notprovenlinkrepair.
- SixACE/SWEETMachOcompilesPASS, SWEETcode/data/relocsunchanged, everyimport
  availableinactualkernel; exact0095->0096patchfuzz0/bytecomparePASS.
  Private research/ace-ufs-linkpower-20261020. Fullhosttest77878 LIVE, notyet
  complete; focused14controller testsPASS. No0096CIorphoneexecutionyet.
- NEXTpublish0096/fullCIonce aftercommit, recordactualrun/job; buildfresh
  candidate/allpreflights andfixedv3controller trial. Latestphoneverified
  firmwareFastboot/installed299251...d17e, root/vendorreceiptretained. GoalACTIVE.

## LATEST ACTUAL0095: first NOP provokes powerfatal +PA_INIT/replay error (2026-10-20)

- CURRENTinstalledboot_b299251071d21fe74c15cae240d6e6ffeda4df11ad5268821cab4c948acd6d17e,
  token7c7a6e5603abff85; actualrootreadback+unchangedvendorreceipt verified.
  NativeSHA7301762855b1a6f98ea5cb109d438ffc2cf750183ade91b5f811284e2b69aa43. No restore/protectedwrites.
- Cold errorscleared again; DMApa142df4000. ActualNOP faultelapsed2586543ticks,
  HCS00000501(PWR_FATAL5), HCE1, DBR0, UTRLRSR0; UTRL00000001:42df4000,
  descriptor0=11000000/OCS05/UCD00000001:42df5000. RequestCRC190a55ad unchanged,
  response512/512 stillA5. UICCMD2 ARG15710000/0/0 (lastDMESET PA_PWRMODE;
  notproof firmwarecommandexecutingnow). FirstfaultPA80000010/DL8000a002
  (PA_INIT +replaytimeout), NL/TL/DME0, IS815; secondwords0/IS815. NoNOPresponse/
  diskread/DMAroundtrip/rootmountproof. Sourceprimaries agreeOCS05peerfailure,
  HCS5fatalpowermode, butexactlink/clock/PHYcause STILLunproven.
- Controller33972 TERMINAL EXIT1 atpre-return recordcomparison, AFTERalllogs/
  root/B/vendor/Androiddiskrefs saved. No rebootcommandissued beforeexception.
  ImmediatefreshUSB+wireless exact288Brecordbothmatched; recordSHA
  9e8575f5bfd9b303e101003a2053bbba4e428afd1d4c7cbb69defe98d7df89c9.
  Originalmismatchbyteswerenotretained: do NOTclaimempty/partialcauseproven.
  Privatefinish-return18820 TERMINAL SUCCESS refreshedidentity/currentrecord,
  finished onlythatnot-yet-issuedreturn, physicallyverifiedFWFastboot/B/unlocked/
  is-userspace=no. Originalexit1 preservedinstate; no keys/controllerrestart.
- Inspector+AEE56860 TERMINAL SUCCESS: currentpmsg8645B SHA
  bd55ec7f89fdd8adf1d1cb05cac0206cadf08923f53f4bf8195b96b74413a3fa,
  all55AEEentriesCRC+sizeverified/rawpstorebyteidentical; archiveSHA
  f617278901dc160ab88554c54a74ff4004191004fe015b88c86930b37e34f928.
  Evidenceprivatephone-trial/actual-ufs-commandfault-evidence.json.
- Controller nowretains everyreturnrecord +refreshidentity; malformed/incomplete
  readobservationsatmost3, COMPLETEdifferentACEFALL1 recordstopsimmediately.
  Nochange to boundedrebootretry policy.14focusedtestsPASS; v3notyetverified
  inwholehardwaretrial. AGENTSupdated. GoalACTIVE/fulliOSnotachieved.

## LATEST0095 image WRITTEN; automatictrial33972 LIVE (2026-10-20)

- Writer46130 TERMINAL SUCCESS: boot_b64MiB SHA
  299251071d21fe74c15cae240d6e6ffeda4df11ad5268821cab4c948acd6d17e,
  token7c7a6e5603abff85. Sending1.389/Writing0.141/total1.532s. CURRENTimage
  isthiscandidate, notoldercbf904. Nooriginalrestore/slot/GPT/protectedwrites.
- Actualnative77594624B SHA7301762855b1a6f98ea5cb109d438ffc2cf750183ade91b5f811284e2b69aa43; fresh9native/Centry/
  4fallback preflightsPASS, previous242unchangedhosttestbaselineexplicitly
  recorded. ExactCI39379607762/job118485446829/remote2e3b8db...SUCCESS.
- tools/ace-auto-trial.py33972 LIVE with--ufs-reference-snapshots. DoNOT
  restartwriter/consumedcontroller. NEXTwait33972terminal, inspectstate then
  inspect-trial.py +independent-aee.py AFTERreadoutandfirmwareFastboot ready.
  ReadfirstfaultUICwords/HCS/UICCMDargs/elapsedticks/requestCRC/poison.
  Thiscandidatehasnotyetreturnedactualresults. GoalACTIVE/noiOSproof.

## CURRENT0095 CI SUCCESS; native process7601 LIVE (2026-10-20)

- Run39379607762/job118485446829 TERMINAL SUCCESS, artifact12244284169
  exactsource2e3b8db598b3f1006ad94a27cd4da659cd22426d, ZIP SHA
  6331e76b70d44d4f6a7c38a6719ec002677d4c213d79a0a0d8a7d4c6b36886d3.
  Actualkernel17523840B SHAdd5a31084768247283390164de9b288288daf01dc7a2d0abe04c44658754556b;
  newfaultstrings/entrysymbols/cacheABI verified fromlinkedartifact.
- build-and-check.py7601 LIVE (freshnative/9cases/Centry/4fallback/package).
  Do not restart this process. PhoneFastboot deviceidentity stillpresent.
  No0095writeyet; currentboot_bcbf904...50b6cb remainsauthoritative.
- NEXT wait7601terminal, reviewmanifest/writer thenoneguardedboot_bwrite,
  newauto-controller/readrefs, inspectactualfirstfault+independentAEE.
  GoalACTIVE; previousprogress andcurrentacceptedCI are notcompletionproof.

## Shipping UFS binary evidence while0095CI builds (2026-10-20)

- REA/Ghidra opened exactsavedmodule ufs-mediatek-mod.ko SHA
  f064758906893c1e112fde167f5ee3c0b627e62ae6e4b064c0912bf27c7a9a03,
  reused previousmatching snapshot, investigated startup/clocks/refclk.
- Staticsetup_clocks powersPHY thenreferenceclock. refclk on path requests
  SMCc2000276/args8,1, writescontroller+144 request1 and waitsrequest/ackbits
  0/1equal up to3ms. Postlinkstartup adjustsDMEvendorattrs d0a6/d0a1.
  These are shipped-binary pseudocode observations, NOT currentphoneclock
  state or proof ofOCS05cause. Do NOT blindly issueSMCs/reset/clockwrites.
- FullREA evidence+snapshot+findings retainedprivate
  research/ace-ufs-commandfault-20261020/rea-shipping-ufs-*.json; closedsession.
  EvidenceIDs recordedin findings. Next0095actualcommandfault regs still
  needed before choosing recovery. Existing0095CI39379607762 live Build.

## ACTIVE NEXT: 0095 first-command fault CI running (2026-10-20)

- Source localb636948 / remote2e3b8db598b3f1006ad94a27cd4da659cd22426d.
  Dispatched ONCE: xnu#14 run39379607762/job118485446829; connector confirms
  live Build step/in_progress. No0095imagewritten. Edge tab590271818 retained
  for unfinished CI. Privateace-ufs-commandfault-20261020/ci-state.json pinsIDs.
- Sixofflineaccept/build/package/prepare/inspect/AEE scripts copied/adapted,
  Python syntax checked, ADT copied. Newlinkedaccept requires fault diagnostic
  strings. Previous installed candidate expectedcbf904...50b6cb and prior
  trialace-ufs-coldhandoff-20261020. 242testlog is explicitly INHERITEDunchanged
  hostpolicy baseline; this log-onlykernelpatch has sixcompile/exactpatchchecks,
  not a new full242test run. host-tests-basis.json records that distinction.
- NEXT poll exactCI; onSUCCESS verifyactualartifactdigest+sourceSHA/linked
  strings/cacheABI; accept-kernel.py, build-and-check.py fresh9cases/Centry/
  4fallback; review concretewriter, oneboot_bwrite, run fixedauto-controller
  with--ufs-reference-snapshots. Inspect firstfault HCS/HCE/UICwords+CMDargs/
  elapsedticks/descriptor/requestCRC/responsepoison toselecttargetedrecovery.
  Do not blindly retry NOP, change address/type, resetlink, or label OCSchange
  genuineNOP success. Latestphone remainsfirmwareFastboot/installedcbf904...
  with actualreadback andunchangedvendorreceipt. No restore/protectedwrites.
- Processes20665/37186/4198/82009/10689 allTERMINAL SUCCESS. GoalACTIVE.
  Previous turn made realhardware+sourceprogress, not a blocker/wait-only turn.
  No XNUblockread, rootmount or usableiOS proof. PreserveRAMdiagnosticfallback
  prerequisite beforeuserdata root write. Fullgoalunchanged.

## LATEST ACTUAL 0094 PHONE: cold errors cleared; first NOP peer failure (2026-10-20)

- Automatic controller4198 TERMINAL SUCCESS, diagnosticADB76.1s, token0ad988cbda359251.
  Root boot_breadback cbf904804f537f9e079fe298c4737018afe4a1f03903a313a4c145f50050b6cb
  and vendor_boot_b unchangedbb5a094...9670 verified. CURRENTinstalledthisimage;
  firmwareFastboot product/B/unlocked/is-userspace=no verified after automatic
  return. Newcontroller2c6ac6150353c19c043d44fd8b5a2840800f5153e1fd9e8898e706c0502f9ac5
  physically handled exact no-device failure then freshidentity/token-bound
  secondreboot succeeded (returncodes1,0). No userkeys/controllerrestart/restore.
- Actual UFS cold1 PA80000011/DL80005800/NL0/TL0/DME0/IS4; cold2 allzero/IS4;
  isolatedUICack; cold3 allzero/IS0. Hostready/idle. Permanent16KiB DMApa142df0000;
  submitNOP then OCS05, responseallA5, IS00000815. This means NOgenuineNOP/
  responseDMA/blockread/rootmountproof. OCS05 isPEER_COMM_FAILURE per pinned
  OnePlusUFSHCI source; IS includesDEVICE_FATAL/UIC_ERROR/POWER_MODE/completion.
  Do not assume link/noDMA rootcause fromthisalone. Wirecommandtype1 correct
  for observedHCI2.0 per sameprimarydriver; do notblindlychange tolegacytype2.
- Pmsg8102B SHAb96e1341bbea923b2fc29e4bfc6786d10f3bf650fb3a9627514c06e689ad4176.
  IndependentAEE82009 TERMINAL SUCCESS:55entriesallCRC+lengthverified,
  rawpstorebyte-identical; archiveSHA6f460159a8540028986233d7221180298feffef04ccfb776c44a6104e0144bad,
  TFAwatchdog38.143411s. Readoutrecord288B SHA2545ebdcb9f9c870a1e5bf7f3e04f17a704c85f40bb2efb4e496baf9197460bc.
  Evidence research/ace-ufs-coldhandoff-20261020/phone-trial/actual-ufs-coldhandoff-evidence.json.
- New0095 adds FIRSTfault two UICread-clears, HCS/HCE/queue/UICCMDargs,
  elapsedticks/requestCRC/responsepoison count BEFOREcompletionack. No new
  queuewrite/reset/retry/CDB/address changes, no acceptance-gate relaxation.
  SixACE/SWEETMachOcompilesPASS/unchangedSWEET/allimportsmatch actualkernel;
  exactpatchfuzz0+bytecomparisonPASS. Privateace-ufs-commandfault-20261020.
  NotfullCI/phoneverified yet. NEXTpublish0095/fullCI thenfreshcandidate/
  allpreflights/guardedboot_bonce/newauto-controller; inspect firstfault words
  to choose actuallink/power recovery, notblindNOP retries. GoalACTIVE.

## LATEST 0094 WRITTEN; physical automatic trial4198 LIVE (2026-10-20)

- Guarded writer37186 TERMINAL SUCCESS: boot_b64MiB SHA
  cbf904804f537f9e079fe298c4737018afe4a1f03903a313a4c145f50050b6cb,
  token0ad988cbda359251. Sending1.389s/Writing0.142s/total1.532s. This is
  authoritative installed candidate, NOT older7338. Onlyboot_bwritten;
  no restore/slot/GPT/userdata/vendor_boot/vbmeta/bootloader writes.
- NativeImage77594624B SHA0349dfc99bb719ae31c31a211bd3902753af9c91532362990c6c4fbe1ba3ddce.
  Fresh9nativecases/Centry/4realAndroidfallbackguardsPASS; package242tests.
- Fixed tools/ace-auto-trial.py process4198 LIVE with--ufs-reference-snapshots.
  Do NOT restart consumed controller/writer. NEXT wait4198terminal, inspect
  phone-trial/state.json, then run inspect-trial.py and independent-aee.py
  only after complete readout+firmwareFastboot. CheckthreeUICsnapshots and
  actualNOP/DMA/LUN2blocks vs independentlycollectedAndroidrefs.
- No phone results from this version yet. CI39377991334/job118480360435PASS.
  GoalACTIVE, no usableiOS/diskread/rootmount proof.

## CURRENT 0094 full CI SUCCESS; fresh native verification running (2026-10-20)

- Run39377991334/job118480360435 TERMINAL SUCCESS; remote6d0bc6dc5651d2b76d1658e7312b5c9f5966a3ab
  verified by artifact workflow SHA. Artifact12243862757 ZIP SHA
  d950cd8007311ae5c650d938bd2ba4de1c85cde74d5cd3f263b4643aff8d6e47.
- Actual linked kernel17523840B SHAefcd27c2e1666ed69eba9a553e06d68a698e176f4be58dd9ed72b1e438d5eb2f,
  new cold snapshot/quiescent/refusal strings+entrysymbols/cachehelper disasm
  independently accepted. No phone execution claim from host checks.
- build-and-check.py process20665 LIVE: freshnative then9cases/Centry/4fallback/
  package/guardedwriter. Do NOT restart while live. No0094write yet; phone
  identity firmwareFastboot/B/unlocked/bootable and backup rehashed this turn.
  NEXT wait exact20665, review candidate/writer then one write +newcontroller.

## ACTIVE HANDOFF (2026-10-20): 0094 published; exact full CI is running

- Local source d90f294; remote 6d0bc6dc5651d2b76d1658e7312b5c9f5966a3ab.
  Dispatched ONCE in logged-in Edge: workflow xnu #13, run39377991334,
  job118480360435. Connector reports in_progress, Build step active; this
  is NOT a successful kernel yet. macOS13.5/DEVELOPMENT/ACE/keep_going=true.
- Private research/ace-ufs-coldhandoff-20261020/ci-state.json records exact
  run/job/source; ci-dispatched.jpg is screenshot proof. Six offline scripts
  copied/adapted and Python syntax checked; ADT copied. No new phone write.
  Acceptance checks new cold sample1/2/3 and quiescent strings, no stale
  LINERESET-only strings. Package requires242 tests; expected previous
  boot_b7338b102...022bc; prior trial is ace-ufs-linereset-20261020.
- NEXT inspect job terminal result, require SUCCESS and exact artifact digest;
  update private ci-state only from observed outcome, download actual artifact,
  run accept-kernel.py then build-and-check.py (9 native/C entry/4 fallback),
  review guarded writer before invoking once, then fixed ace-auto-trial.py
  with --ufs-reference-snapshots. Do not reuse/restart a consumed controller.
  Inspect actual three UIC snapshots/NOP/capacity/blocks vs independent refs.
- Latest phone remains verified firmware Fastboot, installed7338...022bc,
  previous actual readback+unchanged vendor receipt retained. No original
  restore, userdata/GPT/protected writes. No XNU disk-read/root/userspace proof.
- Goal ACTIVE. This turn made actual hardware and source progress; do not
  classify as blocked or complete. Keep data-independent RAM diagnostics a
  prerequisite before future userdata root writes, as documented below.

## CURRENT NEXT SOURCE (2026-10-20):0094 three cold samples +UIC VALID-bit handling

- Newace/ufs_cold_handoff.h mirrorsUFSHCIcodefields (PA1f/DLffff/NL7/TL7f/
  DME1 andVALIDbit31). Rejectunknownreservedbits. Retainedlowcodebits with
  VALID0 are NOTactiveerrors; thisisconsistentwithprimaryufshcd checks.
- Cold-onlyprecondition HCE/HCS/CAP/version/AHIT/idle/bothdoorbells +singleowner.
  ALWAYSsampleallfiveerrorwords twice1msapart. FirstPHY/DLindications only
  areeligibleforread-clear; validDLPA_INIT/NAC/replaytimeout orNL/TL/DME,
  unsupportedISbits/unknownwordbits refuseevenifnextsampleclears. First
  observedPA80000011/DL80005a10 iseligibleONLYifsecondsamplehasNOvaliderror.
  IfneededackpendingIS.UICERROR ONCE, thenthirdsamplemustbequietwithIS0 and
  hoststillready/idle beforeANYownedqueue. Repeated/newerrorsrefuse. Thisis
  anEXPERIMENTALcoldhandoffprobe, no runtimeerrorrecovery, no SMC/reset/
  error-codewrites/diskwrites. No claimthatquietnesshasbeenobservedonphone.
- NewfivepolicytestsPASS, tencontroller testsPASS; full242hosttestsPASS
  30.526s. SixACE/SWEETMachOcompilesPASS/SWEETcode/data/relocsunchanged,
  allimports matchactualAcekernel, full0090..0094exactpatchsequencePASS.
  Controllerhash/version nowpersistedintrialstate; controllerfixnotyettested
  infullnextautomatictrial (priorrebindverifiedonlyseparatescript).
- Private research/ace-ufs-coldhandoff-20261020; no0094imagewritten. Current
  installed7338...022bc/actualroot+vendorreceipt +verifiedFWFastboot remain
  authoritative. NEXTpublish0094/fullCI once, actualkernel +freshnative9cases/
  Centry/4fallback +guardedboot_bonce +fixedauto-controllerwithreferences.
  InspectALLthreeUICsnapshots, actualNOP/high-addressDMA, LUN2capacity/blocks/
  GPTvsAndroid independently. GoalACTIVE, no diskread/iOSroot/userspaceproof.

## LATEST ACTUAL PHONE (2026-10-20):0093 captured different PHY/DL flags; transport return recovered

- CURRENTinstalledboot_b SHA7338b102fb91e81fab31acfb5367ff232699d19954ef76af347acb61e9d022bc,
  token5a3e3b4462cade23. Actualrootreadbackverified +vendor_bootunchanged
  bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670.
  Sending1.391s Writing0.167s total1.559s; onlyboot_bwrite, no slot/GPT/
  protectedpartition/userdatawrite ororiginalrestore. NativeImageSHA
  efa3f8e33670761f458df6de8dcdb381d44bd30600ae1f6cde1d4f334f9c5458.
- ActualHCI: PA80000011 DL80005a10 NL0 TL0 DME0 IS4, HCE1 HCS10f,
  AHIT0/DBRs0/inheritedUTRL51268c00. Exact-onlyLINERESET policy rejected
  beforesecondsample. Thus noDMAallocation/NOP/diskread, notareadsuccess.
  NeedgeneralALWAYSsecondUICsampling and VALID-bitsemantics, preservefatal
  PA_INIT/linklost/unknownflags refusal; do notsilentlyignoreadditionalerrors.
- DiagnosticADB76.1s; allroot/B/bootcomplete/boot+vendorhashes+pstore/dmesg/
  AEE/sdareferencescollected. Controller14698 TERMINAL EXIT1 onfinalADB
  bootloadercommand: explicitdevice-not-found, endpointreturnedimmediately.
  ItwasNOT restarted. Privatefinish-return-fastboot.py checkedfreshserial+
  exact288Bcurrenttoken, issuedthatproved-not-deliveredcommandonce through
  refreshedtransport, thenverifiedphysicalFWFastboot product/B/unlocked/
  is-userspace=no. Script35473 TERMINAL SUCCESS. No userkeys, no reflash or
  extraXNUattempt. Statepreservesoriginal_return_command_failedtrue plus
  transport_refresh_return_verifiedtrue; phase diagnostics-collected-fastboot-ready.
- Actualpmsg7519B SHAef1d708aef7fb2fe955f31b49c405bdc126b2322b4b16433d9cd5c5ffce5bcd7.
  IndependentAEEverify process43401 TERMINAL SUCCESS; all55entriesCRC+size
  verified, rawpstore byte-identical. ArchiveSHA1315bc4ac6dd63339c76dd83ecf91957a431e47c6428179e726c39a4261b974d. Evidence private
  research/ace-ufs-linereset-20261020/phone-trial/actual-ufs-linereset-evidence.json.
- Controllerfixnowrefreshesserial-boundtransport+token justbefore reboot;
  retries atmostonce ONLY exactpre-commandno-such-device, observesambiguous
  errors/timeouts withoutanotherreboot, persistsattempts, verifiesfirmware
  is-userspace=no. Tenfocusedcontroller testsPASS; physicallyrefreshedreturn
  verifiedabove, newcontrollerfullnexttrial stillpending. AGENTS updated.
- Kernel0093 CI39374990895/job118471028939SUCCESS, allkernel/nativeprocesses
  terminal. GoalACTIVE; latestphoneverifiedFWFastboot. No usableiOS proof.

## Current0093 CI milestone (2026-10-20): fullCI SUCCESS; nativeverification live

- CI39374990895/job118471028939 TERMINAL SUCCESS, remote
  cbe516d1037d7288b8b9c131a7feee6a7eaf47f6. Artifact12242757595 ZIP60876846B
  SHA6499fb17fee5039d2f3632b47db82d776aa45e406c6442b8600362873ab86bf9.
  Actualkernel17556608B SHAdd266707092b39131a880ef869f99a1eb6e4cd785d805b440c738536ad0169d1;
  boundstartupLINERESET/resample/cleared/LUN2strings +entrysymbols +actual
  dc civac/dsb cachehelperverified. Nativeverification process97536 LIVE,
  do notrestartonobservationyield. No0093phonewriteyet; installedDEE890...
  currentactualreceipt remainsauthoritative. Followingtheestablishedpipeline.

## RAMdiagnostic overlay source facts (hostonly,2026-10-20)

- AOSPofficialvendor_boot/generic_boot documentation saysgenericramdisk is
  concatenatedaftervendor andoverlaysitsfiletree. This supportsinvestigating
  boot_b-onlyoverlay, NOTproofexactPGKM10diagnosticboot. Officialreference:
  https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions
- Verifiedoriginalvendorarchive has /init symlink->/system/bin/init, actual
  initELF2097264B; recoveryinit.rc importsinit.recovery.mt6895.rc +agingrc;
  userdataext4mountlineCOMMENTED inrecoveryrc, but fullinit/module/gadget/
  filesystemsideeffects stillneedwhitelistreview. Existingadbdservice uses
  recoverylabel/banner; don'tassumeproductionadbdwillprovideusableUID0.
- Recoverymodulelist includesphy-mtk-xsphy,usb_boost,mtu3,xhci-mtk-hcd,
  usb_dp_selector,extcon-mtk-usb; dependencyclosure notyetvalidated. Allfacts
  private ramdisk-init-usb-source-facts.json, noarchive/device modification.

## Futureuserdata-independent diagnostic inventory (hostonly,2026-10-20)

- Verifiedoriginalvendor_boot_bSHA bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670;
  decompressed/readCPIO929entries OFFLINE, no protectedpartitionwrites.
  Originalramdisk contains adbd2108208B, linker64, init.rc, recoverymodule
  lists, matchingmtu3/phy-mtk-xsphy modules. Hashinventory private
  research/ace-ufs-linereset-20261020/original-vendor-ramdisk-inventory.json.
- Thismakes boot_b-only RAMdiagnostic investigationconcrete; doesNOTprove
  successfulrootADB ordata-independentdeviceboot. Preservevendor_boot.
  Need generic/vendor overlayorder +init/module/USB/libdependencies, hostkey
  auth, physicallyverifiednonpersistentstartup BEFOREuserdataHFSwrite.
  Currentauto-trialnormalAndroidbootcomplete/root/SU checks dependon/data;
  futureramdiskdiagnosticmustuseexplicitprofile/identitychecks, neverfake
  AndroidbootcompletionorclaimuserspaceiOS. Keepcurrentactualpipelinefornow.
- AndroidLUN2first8192Bhash63ad1b69531b9d4f87cc88e836126d2c5ebc382118f61f156905c18f156ca9d6
  byte-identicalbetweenthelasttwoactualtrials; no observedGPTheaderdrift.

## CURRENT NEXT SOURCE (2026-10-20):0093 bounded startup LINERESET read-clear verification

- Addsace/ufs_boot_handoff.h copiedbyte-identical intonewkernelpatch0093.
  ONLYexactinitialPA80000010/otherlayersempty/no fatal-linklost iseligible.
  FirstverifyinheritedHCE/HCS/idle/AHIT/CAP/version andsingleowner, wait1ms,
  readALL5errorregs ONCEagain. Mustbeemptyandhoststillready/idle; repeated
  LINERESET/otherbits/unknown/fatal refuse. Noreset/SMC/errorcodewrites.
  ThenexistingemptyIS.UICackoncepolicy appliesifneeded, beforeownedDMA/NOP.
  ExtraHCE/HCS/IS/idle/AHITcheckafterDMAallocationbeforeANYqueuewrites.
- 229hostchecksPASS32.377s, focusednewhandoff4testsPASS; sixlocalACE/SWEET
  MachOcompilesPASS/SWEETcode/data/relocationsunchanged; everynewimportin
  actuallinkedpriorAcekernel. Full0090..0093patchsequence exactfilesPASS.
  Private research/ace-ufs-linereset-20261020. No0093phonewriteyet; read-clear
  HYPOTHESISneedsactualsecondsample, notprovedbyhosttests/familysource.
- Source0093 local8fbfd07, remote cbe516d1037d7288b8b9c131a7feee6a7eaf47f6.
  FullACE CI39374990895/job118471028939 dispatchedONCE and VERIFIED LIVE
  in_progress atBuild viaGitHubconnector; pollthisrun, do notre-dispatch.
- CurrentphoneverifiedFastboot, installedDEE890...181318 withactualreadback.
  No localprocessfor0093lefttopoll. NEXTawaitexistingCI39374990895,
  acceptnewkernel, freshnative9cases/Centry/4Androidfallback, guardedboot_bONCE
  boundactualDEE890...receipt+freshmarkerabsence, mandatoryautocontroller
  withdiskreferences. Inspectpost-LINERESETsnapshot andonlyactualNOP/OCS/
  LUN2blocksCRC/GPTvsAndroidreference. GoalACTIVE; noDMA/root/userspaceyet.

## LATEST ACTUAL PHONE RESULT (2026-10-20):0092 identifies exact PHY LINERESET; no DMA yet

- CURRENTinstalledboot_b64MiB SHAdee89027e7aa306fa36dd792f2bd59b4bb6f463ed2791f90dfb25cb222181318,
  tokend6ac6056c9af93d7. ActualrootreadbackVERIFIED, vendor_boot_b unchanged
  bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670.
  GuardedwriteONCE Sending1.388s Writing0.149s total1.538s, no otherpartitions/
  slot/GPTwrites, no originalrestore. NativeImage77594624B SHA
  837b289d0a3f7e60da88d485d287314bb6abe2212e4f763d155dd573d7860547.
- Controller33399 TERMINAL SUCCESS, diagnosticADB76.1s, root/B/bootcomplete/
  exactboot+vendorhashes +pstore/dmesg/AEE/diskreferences->automaticFastboot.
  phase diagnostics-collected-fastboot-ready/automatic_loop_verifiedtrue.
  No manualkeys. 288B recordSHA2302471b1c08235e88b4ce1128ba34f5e2d2866f341e0ff3ca0cc972baa480cf.
- REALcurrenttokenXNU UFS: IS0, HCS10f HCE1 CAP3587071f/VER200; inherited
  UTRL00000000:51268c00, TM0, DBRs0, AHIT0. Exactfiveerrorcodes:
  PA80000010 DL0 NL0 TL0 DME0, IS0. Priorstrictpolicy refusedmeaningfulcode,
  noqueuewrites, noallocation/NOP/DMA/blockread. LastXNUstillsetconf.
  This identifies LINERESET, notproofthatitisharmlessoralreadycleared.
- Actualpmsg7519B SHA8216f77c5c49a5084e605bfc36c98a8e2eba05c920673886536a2b02bcd1b1e2;
  independentAEEall55entriesCRC+length +rawpstore byte-identical. ArchiveSHA
  1c7fb0b8a3a9854044ac01dc74fefa3a144681eaaa3634ee37bdc997261f8c14.
  Watchdog38.137021s, cpu_idlePCfffffe0007491a9c. Rawproof private
  research/ace-ufs-uic-20261020/phone-trial/actual-ufs-lun2-evidence.json and
  aee-current-verified/evidence.json. Inspectionsession55736 TERMINAL success.
- PrimarypinnedOnePlusfamilysource627e10... ufshcd_link_startup explicitly
  readsUECPAonce afterLINK_STARTUP toclearLINERESET. Referenceonly, notexact
  shippingPGKM10proof. URLhttps://raw.githubusercontent.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/627e10bcc7a36ce80ca9ac834fde02153f73571d/drivers/scsi/ufs/ufshcd.c
  NeedactualsecondUICsample beforetreatingtheobservedstartupindicationasdrained.

## Current0092 build milestone (2026-10-20): fullCI SUCCESS; native verification running

- ExistingCI39373144179/job118465264814 nowTERMINAL SUCCESS. No redispatch.
  Remote f331712461461cedf667da7b181747f5130332f6. Artifact12242740140 ZIP
 60846932B SHA750301436f1fe28e2a388c2a9ac2a62cfd11b8cb46bcd7bfbfd6d4639418a130.
  Actualkernel17523728B SHAe2384d9a5861184947c2cb1703763732bbe2f4aea42e1c8f4297dc5688aa862c;
  linkedUICsnapshot/empty-event/LUN2 strings, entrysymbols andactualdc civac/
  dsb cachefunction verified. Nativebuild+9cases/Centry/4fallback session35048
  RUNNING; neverrestart merelybecauseanobservationyields.
- CURRENTphone remainsFastboot withinstalled1aaaea...9547f. No0092writeyet.
  Exactcandidate/trialstate will bepreparedbyexisting build-and-check.py.

## Current goalturn audit (2026-10-20): prior turn PROGRESS; existing0092 CI verified live

- Re-readcurrenthandoff/AGENTS; previousgoalturn madeconcreteprogress:
  newactualUICrefusal+AndroidLUN2/GPTreference evidence, new0092code/tests,
  liveCI39373144179/job118465264814. ThisturnrevalidatedsamejobLIVE atBuild,
  didnotredispatch. ExpectedUSBphone currentlyFastboot, no newwriteyet.
- Independently rehashed BOTH localiOSrootfiles now: raw16GiB
  7a5ce57e698b0724db024dece682c33f02e307d4ab6ad8da6336aa2af3052775;
  sparse12145303892B b13d9d86c4aa1d22ba0e117e044130f579e717d88aeafa57296f75202c1811d4.
  Actualchecks research/ace-ufs-uic-20261020/root-image-revalidation.json;
  hostintegrityonly, notAceuserspaceboot. Hashsession55751 TERMINAL success.
- IMPORTANT beforeanyfutureuserdataoverwrite: currentautoAndroiddiagnostic
  depends onMagisk/data/services and/data/vendor/aee_exp. HFSuserdata would
  breaktheseassumptions andmaytriggerAndroidformat/recovery. Need physically
  verify an independent no-persistent-data diagnosticUSB/readout path FIRST;
  do notwriteiOSrootjustbecauseboundedSCSIreadpasses. Thisis realdependency,
  notnewapprovalrequest orhypotheticalwarning. Keepvendor_bootprotected.
  Existingtools/ace-recovery-diag.py describesOFFLINEvendor_bootdiagnostics;
  NOTauthorizedtoflashthatprotectedpartition, notprovedstandalonefallback.
  Explore boot_b-onlygenericramdisk/init USBdiagnosticswhenreadpathestablished.

## CURRENT NEXT CANDIDATE (2026-10-20): UIC snapshots / strict empty-event acknowledgement / LUN2

- New0092 +ace/ufs_uic_policy.h recordsallfiveUICerrorregs beforeownership,
  rejectsanymeaningfulORunknownbits evenifISalreadyclear. Onlyemptycodewords
  (0 orvalidbit31alone) permit isolatedIS.UIC_ERROR W1CackONCE, thenbounded
  poll+ready/idle recheck. Never resetslink/SMC or suppressesknownlane/LINERESET/
  DL/NL/TL/DMEerrors. Fatalmask nowalsoincludesDEVICE_FATAL_ERRORbit0x800;
  newerrorpolicy rejects0x804 aswellascontroller/system/crypto/linklost.
- READprobecommands afterNOP nowtarget actualLUN2 (userdisk), not4MiBLUN0.
  Existingwireformat unchanged; onlyboundedread blocks0/1, no disk writes or
  media publication. Queueadoption nowboundedwaitsHCSready aswellasrunbit.
- Host225testsPASS; focusedUICpolicy4testsPASS afterfatalmaskfix; sixMachO
  compilesPASS/SWEETcode+data+relocationsunchanged, allimports matchactual
  priorlinkedkernel. Full0090..0092patchsequence exactsourcecheckedagainafter
  finalmask-onlyedit; PASS. Localprivate research/ace-ufs-uic-20261020.
- Source0092 local5c5a482, remote f331712461461cedf667da7b181747f5130332f6.
  FullACE CI39373144179/job118465264814 VERIFIED LIVE in_progress
  atBuild step viaGitHubconnector; dispatchedONCE. Nextturnpoll thisexisting
  run, do notredispatchorretryoldterminalCI. No localprocesslefttopoll.
- Currentphone remainsverifiedFastboot withactual1aaaea...9547f. No0092
  imagewrittenyet. NEXT awaitexistingCI39373144179, acceptexactnewkernel,
  freshnative9cases/Centry/4fallback, prior1aaaeaactualreadback+markerabsence,
  guardedboot_bONCE+automaticcontrollerwithdiskreferences; inspectUICcodes
  andonlygenuineNOP/OCS/independentLUN2CRC/GPTproof. GoalACTIVE, notusableiOS.

## LATEST ACTUAL TRIAL (2026-10-20): UIC event stopped command ownership; phone back in Fastboot

- CURRENTinstalledboot_b1aaaea5e48769da59941c0000c533316b3716bba9d597ea2746a35f95dd9547f,
  token2e91f0b16a9c4c18. GuardedwriteONCE Sending1.385s Writing0.140s total1.527s.
  NativeImagecbc94b72b5b7c8ea5847843f41510c89d93bae8994ecb8d624675e179643d5a3.
  Controller32269 TERMINAL SUCCESS: diagnosticADB78.1s, root/B/hash/vendor,
  pstore/dmesg/AEE +sda/sdb/sdc8192B reference snapshots, automaticFastboot;
  statephase diagnostics-collected-fastboot-ready/automatic_loop_verifiedtrue.
  No manualkeys, originalrestore or otherpartition/slot/GPTwrite.
- REAL UFS: CAP3587071f VER200 HCS10f HCE1, IS00000004 (UIC_ERROR), IE30e75;
  inheritedUTRL00000000:51268c00, TM0, bothDBR0, AHIT0, bothrunbits1.
  Actualguard said inherited-state gate refused; no queue writes. Thus NO DMA
  allocation/submission/NOP/diskread. Do NOTcall this a read-probe success.
  Need snapshotfiveUICerrorcode regs BEFORE gate, distinguishemptylatched
  event from meaningfulerror; preservefail-closedfornonzero/unknowncodes.
- pmsg7419B SHAb75fe6244e5a4e9fd6990f02b34ab9b7f11c967fd908126584143c39688e8dd9.
  IndependentAEE55entriesCRC+sizeverified +rawring byte-identical; archiveSHA
  1dee6670af6a28a8071f08dfc71d27d542c226608450f937d7fb57dd8c8f7977.
  TFAwatchdog38.137842s, lastXNUsetconf. Record288B SHA
  a548906e4afcaefc033624e7220135a7781e410d66906560b94c695b6a84ca15.
- NEW storage topology fromactualAndroiddmesg +reference: LUN0/sda andLUN1/sdb
  areidentical4MiBbootareas; LUN2/sdc62480384x4096=255919652864bytes isuserdisk.
  Itsfirst8192B SHA63ad1b69531b9d4f87cc88e836126d2c5ebc382118f61f156905c18f156ca9d6;
  primaryGPT EFI PART+headerCRC independentlyverified offline. Referencesare
  Android reads, NOTXNU reads. FuturekernelreadmusttargetLUN2 foruserdata/GPT.
- FullfixedCI39371164720/job118459125511SUCCESS/kernel15b49cb0...c07f9 above.
  AllcurrentprocessesCI/controller/inspectionterminal. GoalACTIVE; actual
  mainline next: UIC error diagnostics +verystrict empty-eventack (never
  suppressmeaningfulUIC/fatalfault), LUN2NOP/TUR/capacity/boundedblocks0/1,
  thenrealbackend/GPT/userdata/rootvolume. NousableiOSverified.

## CURRENT IMPLEMENTATION (2026-10-20): bounded UFS read-command candidate source ready

- Prior goalturn classifiedPROGRESS: actualcontrollerMMIO+automaticphonecycle
  verified below. Currentturn implements separate --ufs-read canonical profile
  (no change to default or priorread-onlyprofiles), new0091 kernelprobe and
  portable ace/ufs_read_protocol.h copiedbyte-identical intokernelpatch.
- Wireformat allows ONLY NOP/TUR/READCAPACITY16/READ10 singleLBA0or1, no
  write/erase/query-set CDB. Purebuilder validatesbeforestores, highaddress
  descriptors,32bytecapacity/512or4096read, responsepoison+1KiBDMAguard.
- Kernelexplicitcommandprofile gates UFSHCI200/HCE1/HCSready/CAP64AS/32slots,
  bothdoorbellsidle/AHIT0/no fatalUICerrors. Snapshotinheritedqueuebases;
  dedicatedpermanent16KiBpage, verifyactualphysical5..8GiB/contiguous/aligned;
  stopqueues+verify, disableIRQ, adoptnewtransferbase+verifybeforedorbelling.
  NoSMC/reset/crypto/media/storagewrites. IdentityDMA remainsHYPOTHESIS until
  genuineNOPresponse; no proofyet. Atimeout retainspermanentpage/stopscommands.
  Bounded500ms +iterationcap perwait. FlushPoC before/aftercommands; actual
  priorlinkedfunction disassembledandhas dc civac/dsb (notcoherencyNOP).
- Source221hostchecksPASS33.939s, sixACE/SWEETMachOcompilesPASS/SWEETunchanged,
  patchsequence0090+0091fuzz0 reproducesexactfinalsources. New2936B ADT.
  Optionalcontroller --ufs-reference-snapshots reads<=8192B eachsda..sdd in
  diagnosticAndroid beforeautomaticFastboot, forindependentCRCcomparison.
  TwoexistingcontrollerchecksPASS afteraddition. No currentturnphonewrite.
- Source2889311; remote0091 commit034228738b6294b7eb895f45fdaf4130ba9907ae.
  FullACE CI39370332016/job118456526974 dispatchedONCE and queued.
  ActualcapturedFDT/new2936B ADT/nativeplatform agreementPASS.
- CI39370332016/job118456526974 TERMINAL FAILED atlink, no newphonewrite.
  Exactundefinedsymbol FlushPoC_DcacheRegion(unsigned long,unsigned long);
  assembly exportsC _FlushPoC_DcacheRegion. Local53425e2 fixed headerexternC
  and corrected sensekey/ASC/ASCQ offsets36/46/47. SixcompilesPASS again,
  newobject importsALLexistinactualpriorlinkedkernel (includingCcachehelper).
  Portableprotocol5checksPASS; wireformatunchanged. Remoteupdated0091commit
  4061f285efb32e0c7615aecb0884a3c68dcede51. NewfullACE CI39371164720/job118459125511 dispatchedONCE and building;
  do notrerunoldfailedcommit or duplicateUI dispatch.
- CorrectedCI39371164720/job118459125511 nowTERMINAL SUCCESS. Artifact
  12241199974 ZIP60843899B SHA10f6e502429ab266b979bc4e34d4d62c70f9173be75d526c0d585b029639550b.
  Actualkernel17523672B SHA15b49cb0ff026fd51795c7c802ee37762fc5d23079db8944369663d8101c07f9;
  boundremotesource4061f285efb32e0c7615aecb0884a3c68dcede51. Actuallinked
  entry/UFSreadstrings/symbols+dc civac/dsb cachehelper verified. Nativebuild
  and9cases/Centry/4fallback currentlyrunning session45530, do NOT restart.
- NEXT finishthisnativeverification, packagefresh
  nativebundle+9cases/Centry/4fallback, bindactualprior1d172...readback and
  freshmarkerabsence, guardedboot_bwriteONCE, controllerwithreferencesflag.
  InspectactualNOP/OCS/response/CRC and independentAndroidbytes; do notclaim
  usableiOS/rootvolume fromreadprobe. Currentinstalledstill1d172...andFastboot.

## ACTIVE handoff (2026-10-20): UFS MMIO DISCOVERY VERIFIED ON PHONE; next actual DMA/command path

- This turn PROGRESS: full0090 kernel built, guarded64MiB boot_b writeONCE,
  complete automatictruephone trial, actualcontrollerregisters +independent
  firmwareCRCproof. GoalACTIVE; no diskread/rootmount/userspace/usableiOS yet.
- CURRENT PHONE is verifiedFastboot afterautomaticADB return. Installedboot_b
  SHA1d172ea1c2f01b95fce99a5d059260dddcf67662601037b5734eaa8dfdf0b905,
  token15500958bbb97933. Rootreadbackverified and vendor_boot_b unchanged
  bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670.
  Sending1.387s Writing0.134s total1.522s; no other partition/slot/GPTwrites,
  no originalbackup restoration. Originalbootbackup stillintactee817627...ed10.
- AUTOLOOP verified again: actualXNUattempt->watchdogreset->same-image pending
  latch diagnosticAndroid->ADB78.1s->bootcomplete/root/B/boot+vendorhashes->
  pstore/dmesg/AEE->ADBbootloader->verifiedFastboot, no manualkeys. Controller
  session6937 TERMINAL exit0; phase diagnostics-collected-fastboot-ready,
  automatic_loop_verifiedtrue. 288B recordSHA7eb50d7653fe0eef77fec71fd8f105bda30479391cc3d36cd00fd486c9619389.
- ACTUAL XNU UFS logs (onecurrenttokenentry):
  ACE UFS: read-only map begin base=0x112b0000 size=0x2300
  ACE UFS: CAP=0x3587071f VER=0x00000200 HCS=0x0000010f HCE=0x00000001
  ACE UFS: IS=0x00000000 IE=0x00030e75 UTRLDBR=0x00000000 UTRLRSR=0x00000001 UTMRLRSR=0x00000001
  ACE UFS: 64AS=1 transfer-slots=32 task-slots=8; discovery only, no media
  This is controllerUFSHCI2.0, NOT deviceUFSprotocolversion proof. Registers
  read through VM_PROT_READ mapping, no MMIOwrites/SMC/reset/DMA. HCE1 and
  runbits1 are inherited firmwarestate, not newlyownedqueues. CAP64AS is a
  capabilitydeclaration, not successfulDMA above4GiB or cache/IOMMUproof.
- Actualpmsg7237B SHAe5fdcb2daf90aa3a2af03ed5e657e5f0bb0a5dacf4d183e116262a98695aa250.
  IndependentHWTarchiveSHA85313e0ea9f755c1485c60a619c4dcd81d2191b6557d51f389afb81354329ac1,
  all55entriesCRC+lengthverified, rawpstore ringbyte-identical toactualpmsg.
  TFAwatchdog38.135861s/CPU0idlePCfffffe0007491a9c. Lastkernelcheckpoint
  still setconf/IOFindBSDRoot, no rootmounted. Actualproof private
  research/ace-ufs-probe-20261020/phone-trial/actual-ufs-evidence.json and
  aee-current-verified/evidence.json; inspection scripts offline+TERMINAL.
- Source0979cad, handoffsf06de4a/7711f09. Remote0090a53f380989eb6a18b8a9cf7ac6a686d0a741580d.
  FullACE CI39368272391/job118449998199 SUCCESS; allprocessesterminal,
  noCI/job/controllerlefttopoll and no needredispatch oldbuild. Artifact
  12240577318 ZIP60831265B SHAd2963a37c686e0ef9975a1dd4c4a6f4f567a5d89174cc095513b8fc6e7c1ba4e.
  Kernel17523360B SHA3ceec4617e5eb02152037dae3a51a13600e6573d930075f88489be9abc7dacdc.
  NativeImage77594624B SHAd6f440db14838172a24568ede4fbe8c21743fe9091910a98365b47e2c08ca5a3.
 215host+2controller tests PASS; sixlocalACE/SWEET compiles/SWEETunchanged,
  actualcapturedFDT/nativeADT agreement, fullkernelentry+UFSlinked symbols,
 9nativecases/actualCentry/4Androidrefusalcases allPASS beforephonewrite.
- NEXT: implement genuine UFS command/DMA ownership and bounded actualread.
  Review observed idle doorbell but activeinheritedtransfer/taskqueues; read
  existingqueuebase/status and sourcevendor/IOMMU/coherency requirements
  before adopting/replacing queues. Use genuineNOP/query and bounded polling,
  prove completion/response and cachecoherency, then SCSIcapacity/read-only
  blocks+GPT/userdata/rootvolume. Do not issue DMA into oldfirmwarequeues or
  assume CAP64AS proves ownership. No fakeIOMedia/RAMroot. RealmanagedRAM5..8GiB.
- Everycandidate uses mandatoryAGENTS automaticworkflow+fresh token; previous
  ACTUALinstalledhash above is nextwriterbasis. Keep experimentalimage, no
  routinebackuprestore. A powerloss or Androidringoverwrite can lose pending
  latch; no blindreboot/reflash ofconsumedtrial. Standinguserwriteauthorization
  supersedesoldgoalobject's per-confirmwording. Protectedpartitionsunchanged.

## Previous implementation milestone (2026-10-20): read-only UFS probe source validated

- Replug observed: exact expected phone is present in Fastboot; no new write
  this milestone. Installed boot_b remains05179f49...226567 and prior auto-loop
  evidence below remains authoritative. No claim of iOS or UFS disk access.
- New0090 Ace-only IOService reads CAP/VER/HCS/HCE/IS/IE/doorbell/run registers
  through permanent VM_PROT_READ MMIO mapping. No MMIO stores, reset/SMC/DMA,
  IRQ setup, media publication or storage writes. Probe can fault on unavailable
  hardware; fresh-token automatic diagnostic path remains required for trial.
- --ufs-probe ADT profile adds root-addressed ace-ufs node only after exact
  liveFDT /soc identity ranges,112b0000+2300, SPI169/GIC and enabled unique
  controller checks. Native canonical validator independently checks resources.
  Default old ADT byte layout stays identical. Manifest adds0090 only opt-in.
- Host215 tests PASS35.544s. Six ACE/SWEET Mach-O object compiles PASS;
  SWEET code/data/relocations unchanged. Patch dry-run fuzz0 and diffcheck PASS.
  Local artifacts research/ace-ufs-probe-20261020/. FullCI/phone probe pending;
  do NOT treat local tests as a true controller observation.
- Local source0979cad; remote0090 commit a53f380989eb6a18b8a9cf7ac6a686d0a741580d.
  FullACE CI39368272391/job118449998199 is building (one dispatch).
  Real captured488371B FDT and opt-in2940B ADT pass native host validation;
  this is source/resource consistency only, not actual MMIO.
- NEXT: await this existingCI,
  accept linked kernel, build opt-in ADT+fresh native image, rerun9nativecases/
  C-entry/4refusal cases with updated native sources, guarded boot_b write once,
  run automatic controller and inspect actual current-token UFS registers.

## ACTIVE handoff (2026-10-20): RTC wait FIX VERIFIED ON PHONE; next MTK UFS/root device

- Latestgoalturn PROGRESS: newfullCIkernel built, candidatechecked, truephone
  testcompleted, RTCservicewaitbypassedphysically, nextrootdevicecheckpoint
  established. GoalACTIVE, NOTcomplete; usableiOS/screens/touch/UFSunfinished.
- CURRENT PHONE expectedFastboot, returnedautomatically aftertrial. CURRENT
  installedboot_b64MiB SHA05179f49f0a61ceedc8391559504a1c5df773cb3ff16a0259d59a1a384226567,
  tokene7071f55bee79e82. Actualrootreadbackmatches; vendor_boot unchanged
  bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670.
  WroteONCE Sending1.386s Writing0.148s total1.535s. No backuprestore/slot/
  userdata/vendor/vbmeta/bootloader/recovery/modem/persist/GPTwrites.
- AUTOLOOP COMPLETE: genuineXNUattempt->watchdogreset->same-image pendinglatch
  Androiddiagnostic5/-67->ADB78.1s->Androidcomplete/root/B/hash/pstore/dmesg/
  fullAEEproof->automaticADB->Fastboot. Controller82349 TERMINAL exit0, phase
  diagnostics-collected-fastboot-ready, automatic_loop_verifiedtrue. No userkeys.
  Actual288B SHA9f8cd5e852b45420701491364ebd28ee0e32316f2636b5292b080996dc5233e5.
- REAL FIX PROOF: pmsg6939B SHAca362464f5d2121bf24f9b9863ec53cb342fa244597ac9ba6f278476b79d6e0d,
 1armed+1XNUentrycurrenttoken, oldRTCwait0, calendarend1, vfsinit1,
  HFS627.100.6registered1, networkstackinit1, setconf1, vfs_mountroot0.
  Exactlastcheckpoints:
  ACE init: RTC backend unavailable; calendar begin without service wait
  ACE init: calendar end
  ACE bsd_init: calling vfsinit
  ACE bsd_init: calling net_init_run
  ACE bsd_init: calling inittodr
  ACE bsd_init: calling setconf
  Independent55entry fullCRC+length verified HWT03 SYS_PSTORE_RAW byte-identical;
  archiveSHA6d8b518e3130403e7c3f1900f9f31a20d798dd5fa4375ea5d3208964d04124f4.
  TFAwatchdog38.134289s, cpu_idlePCfffffe0007491a9c/LRfffffe0007491a84;
  MMUon. Source setconf callsIOFindBSDRoot; NO rootmount/userspace proof.
  Calendarinitializationfallback != hardwareRTCdriver; kernelnetworkstack !=
  MTKWiFi. Truefix is unavailableRTCservicewait, not RTC hardware support.
- CURRENTsourceRTCfix0089 local35968da / remote7b7ab595276e0b0dc4f0d0fd29532bd8be9a1ff0.
  Ace skips unavailableIORTCwait, retainsclock_initialize_calendar (platform
  getGMTTimeOfDay0 fallback), nofakeIORTC/nohardwareclockwrites. ACE-onlyBSD
  macroprintf replacesinvisiblekprintf. SixlocalACE/SWEETMach-OcompilesPASS,
  SWEETcode/data/relocationsunchanged, patchapplycheckPASS. FullkernelCI
 39365892897/job118442546958 SUCCESS; artifact12239457742 ZIP60772199B SHA
 6b4f88db5b5797db7a1481a6f17b4710654a38ea79f52c339ff3c1a1811559ac.
  Actualkernel17519736B SHA29ced29d720b2c4a6875ca12158da20c7ecb594074ed52bfb492cc16b0be3304.
  AcceptscriptcheckednewlinkedBSD/skipRTC/calendarstrings+entrysymbols,
  oldwaitbeginstringABSENT. NativeImage77594624B SHA
  ac8aca91a57e397626bf69273a7db2cb33d5c48933af7c080794283e8be82d4c;
 9nativecases/C-entry/4AndroidrefusalcasesPASS. Host212+2controllerchecks
  previouslyPASS, unchangednative sourcebindingreused. AllprocessesTERMINAL,
  noCI/job/localprocesslefttopoll. NO newdispatch needed foroldfix.
- Allcurrentevidence research/ace-xnu-rtcskip-20261020/: linked-kernel.json,
  ci-state.json/native/preflight/c-entry/qemu-verified/boot-candidate/phone-trial.
  Actualphysicalsummary phone-trial/actual-rtc-fix-root-wait-evidence.json;
  state.json/readout-result.json/fastboot-ready.json includeactualreceipt.
- NEXTMAINLINE: implement genuineMTKUFS/rootdevice path. CanonicalADT/platform
  currentlyhasnoAceUFSnode/backend; AceKernelConfigTables registers only
  SweetPlatformExpert(oneplus,ace-mt6895) +SweetCPU(ace,armv8-cpu); QCOMUFS
  pathgatedoffforAce. Startboundedread-onlyCAP/VER/HCE/HCS discovery using
  reviewedactualFDTresources; NO resets/SMCs/DMA/storagewrites withoutconcrete
  validatedstate. Thenrealcommand/DMA/GPT/rootvolume path, notfakeIOMedia or
  substituteRAMroot. ActualXNUmanagedRAM5..8GiB, verifyhardware64ASbeforeDMA.
  UFSHCI CAP64ASmask01000000. userdata stillAndroid, NOiOSrootwrittenyet.
- ActualphoneFDTsha68c811fbaae657372d740c25ff81f03c9763eab3e897b0a7104d624ec598560b;
  ufshci112b0000+2300, syscon112b8000/112bc000, clocks/resets/powerdomain and
  UFS12/18regulators. Facts rtcskip/ufs-fdt-facts.json, declarationsnotliveHCI
  orDMAownershipproof. OfficialOnePlusOSS/android_kernel_5.10_oneplus_mt6895
  pinned627e10bcc7a36ce80ca9ac834fde02153f73571d, branch
  oneplus/mt6895_s_12.1_oneplus_ace_race. ThreeUFS C/headers +hashes saved
  research/ace-ufs-reference-20261020/manifest.json. FAMILYreferenceonly,
  NOTexactPGKM10shippingfirmwareproof; don'tblindlyinvokevendorSMCs.
- LatestuserannotationrequiresAGENTS mandatoryautoworkflow: DONE90efa7a.
  Eachnewcandidate fresh token, --pmsg, --init-empty-pmsg, pinnedAndroid and
  --auto-readout-after-reset; verify9cases/C-entry/4Android/backup/source/hash,
  bindpreviousACTUAL05179...receipt+freshmarkerabsence, guardedboot_bONCE,
  run tools/ace-auto-trial.py. Neverreflashonobservationyield/restartconsumed
  controller. RetainedRAMlatchnotpermanent: Android logs canreplaceit, so
  neverassumeoldcandidatealwaysdiagnostic onanotherreboot. LostRAM/ringoverwrite/
  earliestfirmwarefaultmaystillneedkeys. No routineoriginalbackuprestore.
  Standing userwriteauthorization supersedesoldgoalobject per-stepwording.
- Earlierrealfixes: -noprogress02ec955 physicallyfixedprogressassert. Source7127efa
  automaticwarmresetreadout physicallyverified76.1s then78.1s repeatedly.
 0088observation kernel849c6c.../CI39364098289 provedIORTCwaitbeginonly,
  oldwait30s andwatchdog38.139s; callerthenassessedtimer13MHz~18.09s, nextdeadline
 8.15msfuture. This was NOTtimerIRQdeliveryproof/exactclockoriginequality.
- Fornextlocalcompiles use exact research/ace-xnu-inittrace-20261020/buildtree
  fromCI39364098289/artifact12238677827 ZIPshacc216455e6cfb6215074909e7120002e59f3e0f2d0e65bd60cedb967d7f6b13c,
  apply0089 whenneeded thennewpatch; C++ requires COMMON.CFLAGS +.CXXFLAGS.
  Temporarystore/restore originals aspreviouscompile.py. OrdownloadnewRTCskip
  buildtree ifexactgeneratedheadersnecessary. AllCIartifacts stayprivate.
- Originalbackupboot_b64MiB SHAee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10
  intact. gh authunavailable; authorizedGitHubconnectorwrites+loggedinEdge
  dispatchworking onUnrealXu/ios-sweet codex/ace-initial-platform. Browser590271818
  onCI39365892897, CUAciTab/shotFs handlesmaypersist. No PRcreated.
  REAfullkernelfunctionqueryearliertimeout330s, emptyexport+CLOSED; don't
  repeatfullkernelanalysis orclaim successfulnewREA disassembly. Actualsource
  available, useordinarysourceanalysis/boundedLLVM fornextsteps.

### Previous real stage5 refusal checkpoint (before seeded trial)

- NEW REAL HARDWARE RESULT: candidate6196459a...a393c11 booted its native loader,
  refused at STAGE5 / ERROR-64 / pmsg codec-3 (INVALIDHEADER), then booted exact
  stock Android through the new diagnostic path. Actual288B sysfs property has
  ACEFALL1 + fresh tokenbbc504000c851102 + native magic/version; no synthetic
  receiver. This proves actual CPU/FDT/platform preparation, not XNU execution.
  CPU EL1/SCTLR30d00800/MIDR412fd050/MPIDR81000000/MMFR0101122/CNTFRQ13000000;
  FDT1830nodes9808props;53exclusions;10planned XNUsegments. XNU materialization
  and jump NOT reached: first log append refused before native_record stage6.
- Actual physical layout: native Image40000000..44a00000; stock Android entry
  41400000; diagnostic copied DTB44800000. USB ADB returned28.1s after reboot.
  Android sys.boot_completed1/Bslot/Magiskroot/SELinuxEnforcing. READBACKboot_b
  SHA6196459a8598ea4de4c4fe29281d4ac6e162671e42f479f2bfc143b39a393c11,
  vendor_boot_b SHA bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670 unchanged.
  Current installed image is this EXPERIMENTAL candidate; NO original backup
  restoration. Normal-refusal Android path now PHYSICALLY verified for this
  exact error/load layout, not all early failures/exceptions/XNU hangs.
- Evidence research/ace-xnu-refusal-20261020/phone-trial/: refusal-record.bin,
  refusal-result.json,android-after.txt,state.json. Property SHA256
  5841fc7186c02078c89d73307ae0c7944cb327c28af0bdbd3e99834f8038fbff.
  Observation97166 TERMINAL success; no liveprocess to poll. This turnPROGRESS,
  prior turnPROGRESS; no genuine external blocker and goalACTIVE.
- New seed primitive committed2e3d215: ace/pstore_seed.{c,h}, separate from
  unchanged codec. It initializes ONLY a wholly ZERO64KiB caller-owned zone;
  returns1(new),0(existing reader-valid, byte-preserved),negative(refusal).
  Any nonzero corrupt/unknown zone is untouched. Three focused tests PASS
  0.238s: signature-only exact write+guards, entire-zone nonzero/corrupt
  preservation, null/overflow/wrong-size refusal. This API is NOT YET linked
  or called by native builder/phone image. Currentphone619645... is unchanged.
  E_HEADER-3 alone does NOT prove this particular live zone was all zero.
- NEXT IMPLEMENTATION: add explicit native --init-empty-pmsg flag requiring
  --pmsg, link seed helper, invoke only after liveFDT/pstore/exclusion gates;
  preserve successful initialization status in recordword31 across later
  appends; log original header/decision for nonzero failures. Keep default
  refusal behavior and codec unchanged. Extend native verifier with an actual
  zero-ring->XNU case (8cases for flag), retain corrupt-nonzero refusal and
  valid-ring preservation. Rebuild/verify source/report/hash bindings then
  direct phone write under standing authorization (no new permission question).

- NEXT concrete fix: native-only OPTIONAL initialization of a fully ZERO pmsg
  RAM zone after liveFDT/range/alias gates. Preserve valid rings, refuse ANY
  nonzero unknown/corrupt zone; keep general pstore codec's no-initialization
  API unchanged. Record actual header/nonzero outcome, test fullzone corruption
  and exact writes; rebuild actualXNU image, run QEMU zero-ring success plus
  valid/corrupt preservation and Android-refusal readback before direct next
  phone write under standing authorization. Do not merely ignore log errors.
  Full iOS/MTK storage/display/touch still unfinished; no hardwareXNUproof yet.

### Earlier refusal-diagnostic build/write checkpoints

- NEW USER AUTHORIZATION2026-10-20: explicitly remove per-write confirmation;
  proceed directly within project scope after concrete image/hash/device/backup
  checks. AGENTS.md and README updated; protected partitions/GPT remain excluded,
  no routine backup restoration. This supersedes older per-step approval rules
  below and in old manifests. Keep full usable-iOS goal, not Android-only success.
- NEW CODE milestone2a1791e: optional normal-refusal handoff to byte-identical
  current Android, carrying token/stage/error in copied FDT chosen property.
  Preserves original DTB/reserves/kernel/pstore header; early entry gates,
  exceptions and XNU hangs DO NOT forward. New low Image numerical bound45000000
  below captured LK mb_kernel end47c80000; firmware/DMA ownership not established.
- Evidence research/ace-xnu-refusal-20261020/: native Image77594624B SHA
  a7835414b01ef7456f141d088c2094427446ba64b1899a03c526dd3e30bf8f2a,
  real XNU SHA c1232a8d...e18f366 unchangedCI39308647764;
  Android Image49185772B SHA8d555ba2...2f11d0 unchanged. Tokenbbc504000c851102.
  ALL203host tests PASS38.187s;7loader QEMU cases PASS, actual16K XNU arm_init
  first instruction PASS. Four fallback QEMU cases PASS:2real native refusals
  boot stock Linux and guest PID1 reads matching288B property;2alignment/alias
  guards refuse without output-DTB writes. Reports preflight/,c-entry/,qemu-verified/.
  Earlier harness failures retained qemu/ (one-byte debugger dump truncation,
  test PID1 BSS ELF issue),qemu-v2/ (sysfs not mounted); repaired fixture only,
  final guest readback PASS. These are NOT physical XNU/iOS proof.
- CURRENT NEW PHONE TRIAL: user approved specific candidate then granted standing
  authorization. Final Fastboot identity/product/Bslot/unlocked/geometry and
  hostimage/backup/source/reports checks PASS. WROTEboot_b ONCE:6196459a8598ea4de4c4fe29281d4ac6e162671e42f479f2bfc143b39a393c11,
  64MiB SendingOKAY1.383s WritingOKAY0.134s total1.519s. Normal reboot accepted;
  USB ADB observation running specific execsession97166 (inspect live handle,
  do not restart solely for timeout). No backup restore/other partition/slot write.
  Phone trial evidence phone-trial/state.json + flash/reboot/preflight logs.
- NEXT: poll existing observation; ifADB returns, root-read
  /sys/firmware/devicetree/base/chosen/ace,native-refusal, require288B+ACEFALL1+
  tokenbbc504000c851102, native record magic/version and exact stage/error.
  Verify actualboot_b619645... and vendor_boot_b unchanged, Bslot/bootcompleted.
  Android return would prove refusal diagnostics, NOT XNU success. IfnoADB,
  inspect realUSB/screen/Fastboot and preserve candidate; no automatic restore.

### Prior trial2 checkpoint (superseded by newest phone trial above)

- LATEST PHYSICAL MILESTONE (source commitb4e8d0c): human specifically approved
  candidate2bf31f3f...727d9c7 and replugged USB. Fresh Android1/Bslot/root/
  SELinux/hash preflight PASS, originalee817... current before write. Pretrial
  pstore/aee captured, newtoken absent. Expected bootloader/product/Bslot/
  unlocked/userspaceno/64MiB checks PASS. WROTEboot_b ONCE: Sending65536KB
  OKAY1.374s, WritingOKAY0.143s, total1.519s. Normal reboot accepted. No other
  partition write/erase/slot switch. This specific write consent is CONSUMED.
- Actual55s USB observation noADB/noFastboot. User reported OnePlus logo then
  black screen; cannot infer XNU success or exact refusal. User then entered
  Fastboot with known buttons and released all keys. CURRENT phone FASTBOOT,
  Bslot, successfulyes/unbootableno/retry1; candidate2bf31f3f... remains installed
  per successful write (no postwrite raw hash readback available). NO original
  restore attempted: follow new retain-experimental workflow.
- Read-only exactLK command oem dump_pllk_log was statically checked: handler
  0x6f50 reads existing buffer pointers at helpers1e264/1e270 and emits20-byte
  INFO chunks; no partition write in bounded handler. Real export SUCCESS
  rc0,314113B,0.752s. Reassembled current PL/LK logs have NO previous TFA CPU0
  PC/LR/SP; boot reason status0x800 after manual reset. Thus diagnostic PC of
  THIS trial is still unavailable. Do not assert error-64 or physicalXNUboot.
- Private evidence phone-trial2-haltpc/: state.json, android-before.txt,
  pstore-before.tar,aee-before.txt,bootloader-preflight.json,flash-candidate.log,
  reboot-candidate.log,usb-observation.json,posttrial-bootloader-state.json,
  bootloader-pllk-{log,joined}.txt,read-bootloader-log.py and bounded static
  command report. USB observation/log-export processes TERMINAL; no livejob.
- A-slot alternate boot reviewed but NOT executed: A backup kernel5.10.226
  (2025-08), no Magisk markers; B original5.10.236(2026-02), Magisk present.
  Current A flags successfulyes/unbootableno do not establish readable/rooted
  Android or safe downgrade. No new approval requested for an unsuitable plan.
- NEXT concrete engineering: implement/review an OPTIONAL native-refusal
  diagnostic handoff to byte-identical existing Android kernel while KEEPING
  experimental boot image installed. Carry stage/error/token through a bounded
  copy of incoming FDT chosen property so Android can read it; no boot partition
  restoration. Existing stock-chain prefix verified relocated-stock execution
  provides a reference, not proof this new path is safe. Current native Image
  has NO such fallback. Need investigate low-boot-RAM ownership/load limits,
  exact original-kernel/ramdisk compatibility, all refusal/alias cases and actual
  QEMU Android execution before packaging/proposing any further phone write.
  Current candidate remains in Fastboot while engineering continues. Full iOS
  goal unchanged, no working MTK UFS/display/touch or iOS userland yet.
- This goal turn PROGRESS: real55-entry crash extraction, codeb4e8d0c, verified
  diagnostic artifact, authorized physical trial and readonly firmware log.
  No genuine repeated impasse: safe host engineering next. Goal ACTIVE.

### Earlier checkpoints before trial2 (device status superseded above)

- NEW PROGRESS after docs commit208e392: actual phone /vendor/lib64/libaedv.so
  readonly capture103208B SHA ded2e7f89f707ae2ae6de64552046b111e94cb0e4ab91fd399443a8555327189.
  REA resolved byte-delta wrapper plus nonstandard ZIP encryption header (zero
  header CRC supplied); full decrypted contents independently validated by size
  and CRC: ALL55 entries PASS. Private reproducible unpack-verified.py binds
  archive/library hashes. Old unresolved-decryption statements below superseded.
- HWT TFA_DEBUG_BUF: watchdog37.844s; at38.845865s CPU0 PC40000114,
  LR40000100, SP4103c8a0; SCTLR30d00800,TCR/TTBR0/TTBR1 all0. These exactly
  match original native.Image native_halt loop branch, native_main return
  address and stack_top. Strongly consistent with native loader refusal; no
  unique trial token found in55 extracted byte buffers, timestamp early-clock,
  so don't claim uniquely attributed XNU or stage/error proof. SYS_PSTORE_RAW
  is0xe0000 bytes, no DBGC; presumed pmsg last0x10000 all zero. Exact clearing
  phase unknown; invalid-ring refusal(-64) is a hypothesis, not established.
- CODE FIX for observability: native_halt now dispatches to bounded8-byte
  WFE/branch slots, PC encodes stage*128+abs(error), stages0..7/exception8,
  error0..127 (unknown/out-of-range127). SP unchanged; no extra memory/MMIO
  writes or checks bypassed. Can decode either instruction PC in slot after
  subtracting actual Image load base + native_halt_slots. Table length9216B.
- New real-kernel native Image native-haltpc/native.Image17326080B SHA
  75aa8435482dec9c358aa650d1336ab2f363debb0723055b9bf9f792f36e7580;
  slots offsets148..2548, new tokenac4d16d6e0c417e9. Seven QEMU loader cases
  PASS (including actual diagnostic PC + unchanged SP for frequency and pmsg
  refusals); actual16K XNU arm_init first instruction PASS;5native tests PASS.
  Evidence qemu-haltpc/verification.json and c-entry-haltpc/verification.json.
  Kernel unchanged, reuse successful CI39308647764; no redundant CI dispatched.
- NEXT PHYSICAL CANDIDATE prepared, NOT flashed: boot-candidate-haltpc/
  experimental-xnu-boot-b.img64MiB SHA
  2bf31f3fdc525f82fa0b17d16106e4c45f0de0422393f6022213d0c0d727d9c7.
  Private package-haltpc-candidate.py verifies CI/source/QEMU/dumps/compression
  bindings, preserves original ramdisk/footer layout; expected currentboot_b
  originalee817...deed10. Human explicitly approved this exact image: 同意本次写入，我在手机旁.
  USB replug restored expected PGKM10 ADB; fresh hash/bootloader checks next. Automatic restore FALSE. All
  protected partitions/backups intact. phone-trial2-haltpc/state.json writes[].
- Latest transport change: readonly vendor library acquisition earlier worked
  through USB ADB; final preflight now NO ADB and NO Fastboot. No new reboot
  or partition write by host. Last verified OS state Android restored; current
  physical screen state unknown. Need actual USB connection before write and
  fresh identity/Bslot/hash verification, even if approval arrives.
- Previous goal turn PROGRESS (workflow commit + recovered ZIP directory);
  current PROGRESS (real archive decrypted, refusal clue, code and verified
  new artifact). Goal ACTIVE, not complete or repeated-blocker threshold.

- USER WORKFLOW CHANGE: retain the latest experimental image between future
  trials and debug it in place; no routine automatic original-boot restoration.
  AGENTS.md and README.md updated. Preserve all partition backups and protected
  partitions. Each destructive operation still follows the existing approval
  rule; no new write is requested or performed in this documentation change.
- CURRENT DEVICE: original backup boot_b was restored exactly once after the
  authorized candidate trial. Read-back SHA256 ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10;
  vendor_boot_b bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670 unchanged.
  Android sys.boot_completed=1, B slot, Magisk root UID0, SELinux Enforcing.
  Candidate 15498cfc...995b78e is CURRENTLY NOT installed. Exactly two boot_b
  writes occurred: candidate once, authorized original restore once; no others.
- Recovery observed: user reached Fastboot via Power+VolUp reset, then hold
  VolDown before Power, release Power at logo and keep VolDown 5–10s. Original
  restore Sending OKAY1.382s / Writing OKAY0.150s / total1.533s. First reboot
  remained Fastboot; after user released all keys, a second normal reboot
  returned Android. Do not rerun the consumed restore guard or candidate write.
- Post-trial pstore is EMPTY; no trial token recovered. This does not establish
  native/XNU execution or prove non-execution. RAM retention across forced
  reset and Fastboot restore download is unverified. No usable iOS yet.
- Read-only HWT archive capture from actual phone is 3197884 bytes SHA256
  a9ab6ab83a24cf9f32e44d8fea499ffb144da98acc660199e56eefbe60d27352.
  REA on actual running vendor producer aee_aedv64_v2 resolved outer transform:
  modified_file_header at 0x140898 XORs first256 and final4096 bytes with
  baa72a51616f151738da4d5436353733. Local reversal yields valid ZIP directory,
  55 encrypted entries. Entry decryption NOT done: historical non-v2 password
  rejected. Actual vendor producer imports ae_db_xx_secret from libaedv.so.
  HWT timestamp is early-clock2010; association with this trial is UNPROVEN.
  REA evidence/snapshot exported and native session CLOSED; no live REA call.
- Evidence private: research/ace-xnu-entrylog-20261020/phone-trial1/
  restoration-verification.json, root-and-hash-after-restore.json, state.json,
  flash-original-backup.log, pstore-after.tar; aee-hwt/finding-ledger.json and
  rea-vendor-producer-{evidence,snapshot}.json. Aggregate verification.json
  updated; preceding version archived. All dumps remain ignored, outside git.
- Next analysis/physical action is the newer halt-PC candidate described above.
  Prior vendor-library extraction next action has been completed. Do not repeat
  unchanged CI or original restore; await concrete approval/USB availability.
- Full-kernel CI39308647764/job118252198439 SUCCESS, source91d962576c40ba56c28eb6712a9a661669d4a5e0;
  kernel SHA c1232a8df639bc0551c69bff9118e4906ea344072ea63ac4e64406e71e18f366.
  Seven loader QEMU cases and actual linked-kernel arm_init first instruction
  passed; 200 host tests passed. These are not physical XNU proof. MTK UFS,
  display/touch and usable iOS userland still unfinished. Goal ACTIVE.

## Historical handoffs below (superseded by active state above)

## Historical handoff (2026-10-20): actual Ace kernel linked; hardware XNU remains unbooted

- Userresumed "继续检查一下", then explicitly reported BLACKSCREEN/no
  display. Fresh USB/ADB/Fastboot AND all wirelessADB/mdns inventory empty;
  hostkerneljournal last10min noUSBevents/errors. Newmanualrecovery
  instructions given: connectedUSB, Power+VolUp10..15s force reset,
  then tryPower+VolDown forFastboot; askedforvibration/logo/mode outcome.
  Force-reset reference official OnePlus10R manual; exactAcebuttonroute
  still needsphysicalconfirmation. No button-resultreply yet.
- New50s button-assistance watcher41239 TERMINAL: noexpectedFastboot;
  guardedalready-authorizedrestore was NOT invoked. Userblackdisplay saved
  instate.json. OriginalbackupSTILLNOTrestored, candidatewrite countONE.
  No newflash/erase/reboot by host. Do not restart watcher just for timeout;
  awaitactualbutton/device-statechange. Authorization continuesvalid; no
  additional approvalrequest needed. Thisresumed audit startsfresh after
  blocked: occurrence1 awaitingphysicalhelp, notlackofconsent. GoalACTIVE.

- CURRENT manual-recovery audit occurrence3 (after013182a): fresh
  recovery-revalidate3.json againNOUSBphone/ADB/Fastboot; no humanbutton
  or screenreply. Prior andcurrentturn NO_PROGRESS; no liveprocess to wait.
  Same genuine physicalassistance blocker now3consecutivegoalturns, so mark
  goalBLOCKED awaitingdevice-statechange/userhelp (not authorization).
  Candidate15498... remainsinstalled; originalbackuprestoreee817... is
  explicitlyapproved and STILLNOTEXECUTED. Do not askagain or flashanother
  image. Resume by inventory; if expectedFastboot then guardedrestore;
  if Recovery/otherUSBmode inspect first. PreservefulliOSgoal and backups.

- Manual-recovery audit occurrence2 (automaticcontinuation afterc3d762d):
  fresh adb/fastboot/lsusb stillNOphone; recovery-revalidate2.json saved.
  State confirms exactlyONEcandidatewrite, restoreauthorized but notstarted.
  No userbutton/screenreply. PreviousturnPROGRESS; thisturnNO_PROGRESS,
  not verifiedwait (no liveprocess). No furtherwrite/erase/rebuild/monitor
  restart or permissionrequest. Cannot perform approvedUSBrestore without
  physicalkey/device-enumerationchange. Blockedthreshold notyetmet; ACTIVE.

- Physicaltrial recovery checkpoint: bounded40sbootobservation and45smanual
  recoveryUSBmonitor both TERMINAL; latestfreshUSBcheck stillnoADB/noFastboot.
  No humanreply to button-assistance question yet; screenstateunknown. Do NOT
  label XNUentrysuccess or originalbackuprestored. Recoverywrite approved,
  pending actualbootloaderenumeration; don'taskpermissionagain. This resumed
  turn isPROGRESS(actualflash/reboot/evidence); manualrecoveryblockeroccurrence1.
  No livebuild/process remains to poll. Do not restartmonitors solely for
  expiredobservation; awaituserbutton/device-statechange. Docs phone-trial
  statusupdated; originaluserlandgoal unchanged, goalACTIVE.

- LIVE PHYSICAL TRIAL (userresumed2026-10-20): human explicitly said
  "开始写入试验镜像、试验后恢复原始备份，继续". This authorizes EXACT
  candidate15498cfc...995b78e and originalrestoreee817627...deed10, not
  arbitrary additional writes. GoalACTIVE; previous blocked audit reset.
- Fresh USBADB preflight PASS: Android1/Bslot/root, currentboot_b=e2d7475e...
  1ed834d andvendor_boot_b=bb5a094d...9839670 unchanged. Both64MiB hostimages
  rehashed; source/QEMUreportbindings rechecked; freshpstore-before.tar
  contains no trialtoken6f45b6931edfabcc. Battery100%. EnterednormalUSB
  bootloader; uniqueexpecteddevice, productk6895v1_64, slotb, unlockedyes,
  userspaceno, maxdownload0x4000000, boot_bsize0x4000000 verified.
- CANDIDATE WRITE EXECUTED ONCE: fastbootflashboot_b15498cfc...995b78e
  Sending65536KB OKAY1.374s, WritingOKAY0.148s, total1.525s. Then
  fastbootreboot accepted. Actual40sUSBobservation: noADB/noFastboot;
  cannot infer actualXNUentry or iOSboot fromdisconnect. Physicalscreen
  state not yet reported. No otherpartitionwritten; noerase/slotchange.
- CURRENT CRITICAL STATE: phone has experimentalXNUboot_b installed,
  originalbackup NOT YET restored. User asked viaasyncquestion to assist
  buttons to returnFastboot; awaiting reply/USBdetection. Need do approved
  restore, not newcandidate/retry. Script phone-trial1/restore-authorized-backup.py
  prepared (NOT executed), guardsonecandidatewrite, approvedbackuphash,
  uniqueidentity/product/Bslot/unlocked/bootloader/64MiB thenwritesEXACT
  originalee817... onceandreboots. Do not re-ask alreadygrantedrestoreapproval.
  Preserve freshstate.json and flashlogs; candidate consent nowconsumed.
- Evidence research/ace-xnu-entrylog-20261020/phone-trial1/ (private):
  authorizationstate, preflight, pstorebefore, bootloadervars, flashlog,
  rebootlog, USBobservations. NEXT detectFastboot (manualassistance needed),
  execute guardedapprovedrestore; waitAndroid; READactualboot_b/vendor_boot_b
  hashes+bootID/SELinux+pstore+dmesg, inspectuniquekernelmarker, reportfacts.

- CURRENT approval audit occurrence3 (after829ea30): still NO replies to
  either specific candidate-write or original-backup-restore question.
  Previous turn NO_PROGRESS; current turn NO_PROGRESS. Worktreeclean;
  all CI/local verification terminal. No new boot authorization can be
  inferred from automatic goal continuation. Same blocker now repeated
  across3consecutivegoalturns, so blocked audit threshold is satisfied;
  mark goal BLOCKED awaiting human confirmations, not complete/paused.
  No further phone/flash/reboot or duplicate CI performed. Resume only
  after actual user input; retain full usable-iOS objective. Future agent
  must revalidate physical presence, current B-slot/hash/USB and evidence
  bindings before any separately authorized partition operation.

- Approval audit (automatic continuation after86d8e46): original request
  turn built realcandidate and requested two specific approvals (condition
  occurrence1, PROGRESS). This continuation occurrence2: neither approval
  has arrived in conversation; worktreeclean, no livebuild to wait on.
  Classification NO_PROGRESS, not a verified process wait. No new hardware
  operation/rebuild/test/duplicate permission request. Next realboot step
  requires those responses and userphysicallypresent; generic continuation
  is not consent. GoalremainsACTIVE; blocked threshold not yet satisfied.

- NEW COMPLETE HOST milestone: CI39308647764/job118252198439 SUCCESS,
  including source+actual-linked-symbol gate; commit91d962576c40ba56c28eb6712a9a661669d4a5e0.
  KernelZIP artifact12213799903 SHA70ed6e9f432e4c64fe7cee7a52871bb4afcb31d3d87d45f1c31b839b66d1accb
  and internalSHA256SUMS verified. Actualkernel17536120B SHA
  c1232a8df639bc0551c69bff9118e4906ea344072ea63ac4e64406e71e18f366.
  Linked676markerbytes EXACTmatch prior executedQEMU fixture.10segments/
  75766localUNSIGNEDpointers. Actual _arm_initVAfffffe0007b237ac,
  early_bootargs_readyVAfffffe00074a03b8. Evidence linked-kernel.json /
  linked-marker-verification.json underresearch/ace-xnu-entrylog-20261020/.
- Fresh-token native Image17317888B SHA
  5edb289a5e3ab5ab669f958e4d49d817928976d9d241d0f1ec25fcf719168e13,
  payloadSHAfa0c36accb530f77a5aebabbd5b9a2c3da091c6940ab0472eaf6c07c3cb2d02d,
  token6f45b6931edfabcc. NewfreshROOTREADONLYphoneFDT still488371B SHA68c811fb...
  98560b. Sevenactualkernelcopy/refusal/relocationQEMUcases PASS including
  three exact token-bound XNU markers, fulltarget/BSS/args/ADT comparison.
- ActualnewXNU16Kbootstrap+firstarm_initCinstruction PASS, markerretained.
  TCR226511a511,TTBR014117c000/TTBR114118000,SPfffffe0007d08000,
  BootArgsKVAfffffe000811c000. Initial C-entry verifier FAILED ring extraction:
  post-MMU GDB interpretedPA48160000asVA. Preservedc-entry-failed-virtual/;
  fixeddebugger physical-read mode ONLY, noImage/kernelchange; current c-entry/
  PASS with currentverifierSHA. OfficialQEMUgdbdocumentationchecked. Full200
  testsPASS44.504s full-tests-linked-final.log; no CI needed forverifierfix.
- CONCRETE64MiB boot_b candidate nowbuilt/HOSTreviewed:
  boot-candidate/experimental-xnu-boot-b.img SHA
  15498cfc252fa390d376dd5aace4b6a77486ea1833f5e994da7c43b3a995b78e.
  Exact originalMagiskramdisk retained; gzipindependentroundtrip, boot-v4/
  fullpartition/footergeometry+oldobsoleteAVBmetadatapreservation checked.
  NOTsigned/workingiOS/Androidfallback. PhysicalLKacceptanceunverified.
  ManifestbindsactualCI/kernel/Image/run-token/QEMUrawdumpchecks.
- Rollbackoriginalboot_b64MiB SHAee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10
  freshlychecked. User-assistedmanualkeyrecovery+actualrestorewriteuntested;
  USBbootloader getvar/reboot path previouslyverified; fastbootbootUNSUPPORTED.
  Phonepstorebaseline rootREADONLY265216Btar/2files, no6f45b6931edfabcc token;
  privatepretrial-pstore.tar/json retained. No code/reboot/partitionwrite.
- NEXT FINAL GATE: docs/ACE-XNU-PHONE-TRIAL.zh-CN.md concrete review ready;
  SEPARATE approvals REQUESTED throughasyncquestion tool for candidatewrite
  AND exactoriginalbackuprestore; no answers yet. Both required before starting.
  Olddiagnosticwriteconsent consumed, neither newwrite authorized yet. Do NOT
  flash absent responses; ensure userphysicallypresent for manualrecovery.
  No physicalXNU/iOSboot, MTKstorage/display/touch/rootfs incomplete. GoalACTIVE.
  Implementation/phone-review committed0052c68. Aggregateverification.json
  bindsCI/kernel/Image/candidate/QEMU/current200tests; ci-complete.jpg saved.
  Previousgoalturn classifiedPROGRESS; thisturnCI+actualkernel/image/candidate
  isPROGRESS. All localprocesses+CI terminal; no livebuild to poll.

- CORRECTION / CURRENT CI: run39307343401/job118247731839 reportedSUCCESS
  but DID NOT APPLY0087: git apply treated /dev/null as a source because
  new-file-mode metadata was missing. POSIX patch dry-run/local compiles had
  passed; that was insufficient pipeline validation. Its kernel is EXCLUDED
  from new-marker/native-phone candidate use. Verified full-log artifact
  12214667161 ZIP SHA8c380d59a1111c290a66f7c2504b4922207a4f992442d127ded855df5bc1425f;
  skipped-build-evidence.json contains exact0087warning; full raw log retained.
- FIX: added new file mode100644, actual CI-style git apply check+application
  regression PASS. Identical676 marker-code bytes, new19caseQEMU matrix PASS.
  Added CI ACE-only gate requiring source file and TWO symbols in actual
  linked kernel via xcrun nm; pipeline cannot silently accept missing0087.
  Current remote branch91d962576c40ba56c28eb6712a9a661669d4a5e0
  (parents4b80a804c1dcd633cce1b36294be1f495c993051,7184736).
  NEW run39308647764/job118252198439 IN_PROGRESS Build at last check.
  ACE/DEVELOPMENT/13.5/macOS14; do NOT redispatch absent actual new failure.
- Local source milestone committeded2ac40; follow-up fixes255e5af. FINAL200testsPASS58.706s full-tests-git-format.log (earlier199
  PASS54.442/50.324 retained). New verifier records dynamic bootargs-ready
  boundary honestly (no false11instruction count for newlogger) and C-entry
  checks token-bound ring survives16K bootstrap. Not yet run on new CI kernel.
- FRESH actualUSB readonly preflight: device/sys.boot_completed1/Bslot/
  SELinuxEnforcing, boot_b still exact authorizeddiagnosticSHAe2d7475e...
  1ed834d. phone-preflight.json; no reboot, code, module or partition write.
- Aggregate verification.json binds200tests/source/evidence; all local
  compiler/QEMU/GDB/test/download processes terminal, ONLY CI39308647764
  still live. Final browser screenshot ci-fixed-dispatched.jpg shows that
  exact run and91d9625. NEXT: finishrun39308647764, download+hashactualkernelZIP, verify linked
  early symbols/marker bytes, buildfresh-token native Image, execute7case
  actualkernelpreflight and actual16K/C-entry verifier. Private host-only
  package-candidate.py prepared but NOT executed; binds commit91d9625 and
  reports before packaging. No new boot candidate exists yet. Only after
  concrete64MiB candidate+rollback review ask individual partition approvals.
  Original restoration remains unapproved, no newflashauthorization consumed.
  No physicalXNU/iOS boot, MTKdrivers/rootfs incomplete. GoalACTIVE.

- NEW entry-marker SOURCE milestone: patch0087 adds ACE-only stackless pmsg
  writer BEFORE OSLAR_EL1. Exact bounded ace_pmsg=1 + ace_run=16lowerhex;
  rejects missing/duplicate/malformed known options, unterminated608B line,
  bad revision/version/control/RAM/ring. Generated ABI0/108/608/736 checked.
  Preserve x0/x17..30; no calls/stack/MMIO/header repair. Fixed known pmsg
  ordinary-RAM ECC0/type0/exclusive ownership remains caller contract.
  New mknative generates fresh build token (explicit reproducible option),
  omits pmsg options if disabled. Reused images reuse tokens: physical trial
  must reject preexisting same marker and use fresh build. Not authentication.
- Real Mach-O start.s compile PASS, generated genassym PASS, SWEET code/data
  sections+relocations unchanged with ACE disabled. 676 marker bytes SHA
  a579d4441d2d0d3f3295dbc0106e94e3866db9cb58f640e7442a93c58ae295c6
  equal QEMU-executed fixture. 19 QEMU append/wrap/refusal cases PASS; full
  199 tests PASS54.442s. Evidence research/ace-xnu-entrylog-20261020/.
  New verifier uses actual _ace_early_bootargs_ready symbol instead of fixed
  11 instruction count and requires one exact bound XNU marker for new kernel.
- Personal fork branch updated minimally (only0087), no private notes/dumps:
  UnrealXu/ios-sweet codex/ace-initial-platform now718473634c2df64177b4b1558dcd5a81fb372cd7.
  Workflow run39307343401/job118247731839 STARTED03:00CST, ACE DEVELOPMENT
  13.5 macos14. In progress at last check, not yet complete; don't redispatch
  merely for stale status. Get final artifacts, validate linked marker,
  rebuild native Image and rerun actual full-entry/C-entry QEMU before phone
  candidate review. Screenshot ci-dispatched.jpg. gh login NOT needed; fork
  connector writes/browser dispatch working. No new phone code/flash/reboot.

- MAJOR native-entry SOURCE milestone: ace/native-loader now is REAL raw
  EL1Image integration, notace/xnu-loader'ssyntheticreceiver. EstablishBSS/
  caller-ownedworkspace/64KiBSP_EL1+guard/VBAR, freshCPUcapture, liveFDTmemory/
  Image-v-firmware/initrd exclusions, canonicalADT, realmaterialize, recapture,
  DSB/IC/ISB andBR actualXNU(x0=BootArgsPA,x1..3=0). EarlyEL2/MCI/EE/
  alignment/loadwindow/pinnedFDT refusal precedesImage-data writes. Requires
  firmwareownsinitialImageRAM+quiescentCPUs/DMA; numericguards don'tproveit.
  Implementation/tests/docs committed3a1e9ff. FinaldiffcheckPASS/worktreeclean.
  Aggregateverification.json bindsactualImage/programsources/archivedruntime
  verifiers/7cases/16KC-entry/full197tests/readonlyphonehealth. No kernelCI
  submitted because linkedXNUe377codeunchanged; nextkernelentryloggerneedsCI.
- tools/ace-mknative.py buildsONLYlocalignoredrawImage+ELF, SHA-boundactual
  kernel/ADT. No phone/boot.img/AVB/signing/flash. Actual artifact image-v2:
  17317888B SHA2139b81b057812fdb14b6871812359c69e8fd430681743781a6f27ad48b3c187.
  Realkernel e3772e867b64b1777488b9e2cf3ca1d5a431a4c7f543b106354d8fe05d98652a
  unchangedCI39288876908; nativepayloadSHA4c3b5c6627a9a83fdf34e393b5caae98abc3d127a9a11e461c6882e63f988f7c
  (commandline debug=0xc serial=3 cpus=1 keepsyms=1 ace_pmsg=1, no spamflag).
  NativephysicalRAM5..8GiB, FDTPA47c80000, text_offset80000, pmsgexplicitON.
- SevenQEMU actual-Imagecases PASS: EL2/wrongFDT beforeBSS refuse; 62.5M
  frequency refusesstage1/-22; invalidDBGC refusesstage5/-64 beforetargetcopy.
  Actualkernelcopy/BR+first11XNUinstructionsPASSat40080000,42000000(oldImage
  overwritten5a),andphone-observed40000000. ALL10segments/966656BSSbytes/gaps/
  full16KiBBootArgs+ADT+pmsgrecordchecked. Refusalcomparesseededloaded-segment
  targetspan/logs, NOT everybyteof3GiBwindow. No syntheticreceiver. CPU model
  cortex-a55,cntfrq=13000000 isQEMUfixture, actualMTKcontrollersNOTmodeled.
- FURTHER actualXNU QEMU result: reaches _arm_initVAfffffe0007b2350c and
  executesfirstCinstructionPCfffffe0007b23510. BootArgsKVAfffffe000811c000,
  SPfffffe0007d08000, TCR226511a511(TG0=2/TG1=1=>16K,IPS2=>40bit),
  TTBR0=14117c000/TTBR1=141180000. Indicatesactual16Kbootstrap exercisedin
  QEMU ONLY; notphoneXNU, IRQ, storage, display, touch oruserland. New
  verify_c_entry.py derivesactualsymbolviaLLVM-nm; boundedGDB/QEMUcleanup.
- NativeEL1vectorsrecordESR/FAR/ELR/SPSR into32Q ACENAT01 Image record;
  XNUreplacesVBAR early soNOTcompletekernelpanictrace. Optionalpmsgordinary
  RAMcodec assumespriorECC0/type0/exclusiveownership; no unknownheaderinit.
  Currentpersistentmarkers PREPARED/ABOUT-TO-BRANCH doNOTprovephoneXNUentry.
  Failuresbeforevalidatedpmsg leaveonlyvolatileImage record. Nohardwaretest
  readyclaim. ActiveMMU/cache/EEassemblyrefusalbranchesnotexecutedthismatrix.
- Developmentfailurespreserved: absentparentoutputdirectory thenfixed;
  -mstrict-align generatedaggregate memcpy despitefno-builtin; initiallink
  failed, memory.c nowprovidesreal exactvolatile-byteABI operation (nostub).
  GDBCNTFRQwriteignored sofirstpreflightpmsgcasecorrectlyfailedfrequency;
  usedpublishedQEMUcpu cntfrq propertyinstead. image/ andqemu-preflight/
  incompleteartifactsretained; image-v2/qemu-preflight-final/c-entry-final
  areauthoritative. No silentupgradeoffailedcaseintopass.
- FINALfull197testsPASS44.212s,3artifact/inputtests+debuggernumber-type
  regression. ExactNativeImage/sourcebindingPASS. Runtimeverifiercopies
  verified-preflight-source.py/verified-c-entry-source.py preservehash-bound
  versions; laterinput-only numeric/pathguardscheckedwithoutchangingImage.
  Privateindependent-copy-audit.json comparesfullloadedspan+args ofearlier
  twocases; final7-caseverifieralreadydoesfullchecksallthreesuccesses.
- Evidence research/ace-native-entry-20261020/: buildlogs,rawImage,payload,
  machine-code/relocations,commands,symbols,7caseRAMdumps+GDBlogs,C-entry
  registers,full-tests-final.log,phone-health.json. FreshreadonlyUSBdevice /
  Androidboot1/SELinuxEnforcing. No phonecodeexecution/reboot/module/flash
  thisphase. Currentdiagnosticboot_bstillinstalled; originalrestoreunapproved.
- PRIORgoalturn classifiedPROGRESS(platform+phoneEL0). NEXT concreteaction:
  addAce-only EARLIEST XNU pmsg marker (prefer beforeOSLAR_EL1 toobservean
  earlytrap), boundedexplicitbootarg optin/preserveBootArgs; buildactualkernel
  viaexistingpersonal-forkCI, auditlinkedmarker+refreshnativepayload. Bind
  uniquephysicalrunmarker, packageconcretereviewableboot_b+rollback before
  askingforoneindividualdestructivewrite. Do NOT call nativeabout-to-branch
  log orQEMU C-entry phoneiOSsuccess. No MTKdrivers/rootfsready. GoalACTIVE.
  All QEMU/compiler/testsessions terminal; no liveCI/REA towaitonthisphase.

- New SOURCE + REAL PHONE EL0 milestone: ace/xnu_platform.c/.h validates
  eightCPUregaffinities/A55+A78/PSCI,uniqueCPU/GIChandles,GICv3addresses,
  fourfulltimerspecs/provider/13MHz andPSCI1.0SMC. Canonical9node2652B ADT
  compare derivesCPUclock/RAM; ALLbytesfixedexceptopaque64Bseed. Notarbitrary
  ADTparser, seedentropyNOTvalidated. New prepare/materialize wrappers gate
  actualcopier, preserveplan/targetonrefusal, rejectcontext/mappingaliases.
  Implementation/tests/docs committed64ed046; finaldiffcheckPASS and
  worktreeclean. No kernelCIretry needed for this native-loader-only change.
- Actual FDT GIC HASppi-partitions: initialnochildassumptionrefused actual
  input; inspectedactualsubtreeandnowcheckstwo4CPUgroups/affinityhandles,
  rejectingunknowncontrollers. AlsofixedtestCPU-node-namepaths(@004not@400);
  actualhardwareIDsarefromreg, notnodename. Fixture nowincludesCPUphandles/
  interrupt-controller flag. No hardwarecontrollerregisteraccessorPSCIcall.
- IMPORTANT native-prep finding: GNU objects emitted8+7 R_AARCH64_ABS64
  data pointers forlocalstringarrays inplatformADTwriter andCMAnamelist.
  Fixed-addressAndroidELFtestwasvalid; flatrelocatedImagewouldneedfixups.
  Replacedpointerarrayswithdirectstringreferences. Final5-objectnativechain
  NOABS64/32/16/MOVWabsolute-datarelocations andNOruntimeimports. Thisisstatic
  evidence only; completebootImage/runtime relocation stillneedsvalidation.
  Pre-fixobjects/findingJSON retained, no existingphonekernelimagechanged.
- FreshliveFDT SHA68c811fbaae657372d740c25ff81f03c9763eab3e897b0a7104d624ec598560b;
  candidateADT SHA25ee9cbdc916eb01f393f686a77e5aeb33038eb5e2437195017e578a23a47033.
  ActualphoneUID2000/CPU0 runs SAMEnewpureCplatformchecker, exit0. Platform
  compare0; truncated/corruptADTboth-45; Androidstagepolicy-32unchangedoutput,
  numericpreLinuxmemoryreplay0. Processmemoryonly, no CPUcapture/materializer/
  XNU/controllerexecution. Latestfinalprobe23840B SHA
  c7f813f6511d69c2f970e2a2670202a473251a1e47e4264caf1164455fc8d830.
  Post-relative-fixbinaryREEXECUTEDphonePASS, all3stagedfiles+directorydeleted,
  samebootID/Android1/Enforcing. No module/reboot/partitionoperation.
- Firstplatformphoneversionff3d67e...alsoPASSfixed-addressELF (saved as
  phone-before-relative-fix.json); finalc7f8versioncontainsrelativesourcefix.
  No claimthatoldphoneELFfailedbecauseofabsolute refs: no nativeImageexecuted.
- 9newregressionsPASS includingASan/UBSan2000FDT+ADTmutations/truncations,
  fulldestinationrefusal/nochanges, PPIgroups, inputaliases, nativeimports/
  absolute-datarelocs. FINALfull193testsPASS42.540s (earlierpre-fixfullPASS
  43.099s retained). Singleframeadt_check3248B/platform352B/prepare1872B/
  materialize1888B; memorypolicy4352B afterarrayfix. Notcompletebootstackbound.
- ActualACEkernelpayload HOSTchainFDTpolicy->CPUfixture->platformcheck->
  actualmaterializerPASS10segments/966656BSS/ADT/BootArgs/53exclusions.
  No kernelinstructionjump. Evidence research/ace-platform-20261020/ incl
  phone-result.json/materialize-verification.json/full-tests-final.log and
  relocationobjects. Docs ACE-XNU-PLATFORM-CHECK.zh-CN.md.
- Previousgoalturn classifiedPROGRESS(nativeFDT+phoneEL0). Nextconcreteaction:
  integrate native ARM64Image entry/BSS/stack +freshCPUcapture +liveFDTpolicy/
  platform +actualpayload, prove runtimeaddress/relocation andearliestXNUtrace;
  assesscoldfirmwarememoryhandoff. Don'taddanothergenericvalidationmilestone
  as substitute forconnectingentry. No deployableiOS/MTKUFS/display/touch yet.
  Originalboot_brestorestillseparateunapproved. No newflashauthorizationused.
  All build/test/phoneprocessesterminal, no liveCI/REA. KeepgoalACTIVE.

- New SOURCE + REAL PHONE EL0 milestone: ace/fdt.c/.h boundedfreestanding
  DTBv17index (2MiB/4096nodes/16384props/depth64), caller282656Bworkspace,
  no allocation/I/O. Bounds/duplicates/tokenorder/end/reservations checked.
  ace/xnu_fdt.c/.h rebuildmemorypolicy fromliveFDT: actualbankcontainment,
  40bit/32MiB, FDT/initrd/header+fixed+dynamicdomains+source+caller exclusions.
  OnlytwoexactknownCMAdeclarations deferred undercallerpreLinuxcontract.
  This is NOT proof of stage, firmware/DMAownership or full CPU/GIC/timer/
  PSCI-to-ADT compatibility. Keep outputinplace (reservedselfpointer).
  Source/tests/docs committed56638ca. FinalgitdiffcheckPASS, worktreeclean;
  no CI submitted because thisphasechangesloader/diagnostics, notXNUkernel.
- FRESH ROOT-READONLY liveFDT capture488371B SHA68c811fbaae657372d740c25ff81f03c9763eab3e897b0a7104d624ec598560b,
  sameaspriorcapture. Real FDT haslastcompatible2 andnonzeroalignmentpadding;
  initial strict16/zeropaddingparser refused. CheckedactualOEM/upstreamlibfdt,
  nowcurrentversion17/last<=17 andboundedignoredpadding; NOT skipping bounds.
- Actual phone finaldiagnostic: diagnostics/ace-fdt-policy sources, UID2000 /
  CPU0 taskset1, rawLinuxsyscalls/no libc/runtimeimports/privilegedMRS/MSR.
  NativeCparser+policyexecute inPROCESSMEMORY only, exit0,1830nodes/9757props,
  53exclusions/twoCMA. Androidstage0 correctlyrefuses-32 withunchangedoutput;
  stage1 is explicitNUMERICREPLAY, notactualcoldboot. No materializer/kernel
  executed onphone. Temporaryfiles+directoryremoved; samebootID/Android1/
  Enforcing. No module/reboot/partition operation. Phone-result.json private.
- Finalprobe11720B SHA1c62ce61e8a97b9c627694bf34f00521e4cb47ca78d5c615743c2c95c19e92cb,
  twoindependentbuilds byteidentical andfinalbinaryreexecutedonphonePASS.
  Addedfixed .file becauseGNUassembler randomtemporaryfilename changedonly
  strtabbytes between otherwiseidenticalbuilds. build.sh defaultsbuildonly,
  no phone connection/download/sudo; separateprivate live.py performedruns.
- INITIAL phoneprobe failedexit139; cleanupPASS. DefaultELF zero-fileBSS
  LOAD hadnonpagealignedoffsetbeyondEOF. ExplicitpagealignedBSSlinkerscript
  fixesexecution; nooriginalfaultPCcaptured, thusELFloadercauseisINFERENCE,
  notclaimedexactinstructiondiagnosis. Rawfailure/artifactpreservedprivate
  phone-first-failure.json, obsolete-default-link-probe. Initiallibccompile
  alsofailedmissingcrossheaders; noinstall, replacedwithrawUAPIverified
  againstexactOEMunistd.h. Don'tsilentlyturnfailedfirstprobeintoaPASS.
- 8newregressionsPASS; finalfull184testsPASS37.463s. ASan/UBSan3000bounded
  mutations/truncations, unchangedinput andunchangedfailedpolicyoutput.
  NativeA55objectsNOundefinedimports; stackusageparse304B/policy4400Bsingle
  frames, NOT entirebootchainbound. Private native-objects/*.su.
- ActualACEkernelpayload now HOST chainFDTpolicy->CPUfixture->actualC
  materializerPASS10segments/966656BSS/ADT/BootArgs,53exclusions. Still
  no nativeCPUcapture/FDT-to-ADTfullplatform/hardwareownership verified.
  Evidence research/ace-native-fdt-20261020/verification.json, rawphone and
  materialize-verification.json; docs/ACE-XNU-FDT.zh-CN.md.
- Prior goalturn classifiedPROGRESS(CPUgate). Currentmilestone makes native
  memorydeclarationvalidation concrete; NOT deployableiOS. Next validate
  liveCPU/GICv3/timerPPI27/PSCI againstADT, integrateactualnativeentry with
  runtimeaddresses andearliestXNUtrace, establishcoldfirmwareownership.
  Originalboot_brestorestillseparateunapproved; noflashrequested/executed.
  All processes terminal, no liveCI/REA, no needkernelCIretry forloaderonly.

- New SOURCE milestone: ace/xnu_cpu.c/.h +xnu_cpu_capture.S gate before actual
  bounded loader; checkEL1/fullaffinity0/A55/16K/40bit/13MHz/LE/MCIoff/DAIFmask.
  Captureleaf readsactiveEL1orEL2SCTLR, noMSR/stack/MMIO/SMC, writescaller56B
  recordonly. EL0 mustNOTcall(CurrentELtraps); onlyzero-returnrecordvalid.
  EL2 gate refuses; transitionstillseparate. RAMnativewrapperlimit40bit.
  No runtimeFDT/firmwareDMAownership/secondaryquiescenceclaim; no bootimage.
  Implementation/tests/docs committed a1367a7; final gitdiffcheckPASS and
  worktreeclean. All test/compiler/QEMU processes terminal, no liveCI/REA.
- 5newtestsPASS; full176testsPASS33.155s. Includes actualsavedprefixvalues
  andAndroidperCPUcaptures asPARTIALobservations, NOT afreshcompletesnapshot.
  Firsttestfound MPIDRreservedhighbitsallowed; fixedbeforefinaltests. Real
  freestandingA55C+assembly+loaderpartiallinkhasNOundefinedruntimesymbols.
- ActualACEpayload viaCPUwrapper materialize0,10segments/966656BSSbytes/
  52reserves/ADT/BootArgsallchecked, HOSTfixtureCPUstateonly. Private
  ace-cpu-gate-20261020/materialize-verification.json. No targetCPUjump.
- QEMU executesactualcapturehelper+sameCcheck: EL1A55records62.5Mtimer/refuses
  -22; EL2A55recordsEL2/refuses-17; EL1A76refusesmodel-19. No syntheticXNU
  receiver/realXNUexecutionclaim. Logs/images/sourcehashes capture/verification.json.
- Fresh readonlyUSBhealth: state=device, Androidboot1, SELinuxEnforcing.
  No insmod/rootrequest/reboot/flash. phone-health.json private. Diagnostic
  boot_b remainsinstalled, originalrestorestillseparateunauthorized. GoalACTIVE.
  Prior goal-turn classifiedPROGRESS(actualCIkernel+ISA/materializationevidence).
  Next: integrate actualnativeentryruntimeFDT/ownership andearliestXNUtrace;
  CPUgatealone doesNOTjustifyphoneRAMwrites or anotherCI/kernelbuild.

- THIRD FULL CI39288876908/job118183995118 COMPLETED SUCCESS, allstepsPASS.
  Personal fork UnrealXu/ios-sweet branchcodex/ace-initial-platform source
  5ea487d7f403efb8739115550098bd568c7069b3. No upstreamwrite/CLIlogin needed.
  https://github.com/UnrealXu/ios-sweet/actions/runs/39288876908
  This supersedes all queued/in-progress observations below. Patch0086 fixes
  the actual BearSSL gate; no further build retry justified by old metadata.
- Actual kernel artifact12205216685 ZIP SHA
  31239ecbfa0079ab1f6072e979716e50558678f9dc72c5f7dd9c08270c3abc94;
  kernel.development.ace17519656bytes SHA
  e3772e867b64b1777488b9e2cf3ca1d5a431a4c7f543b106354d8fe05d98652a.
  ArchiveSHA and internalSHA256SUMS verified. Private ace-linked-20261020/.
  Buildtree12204689246 SHA cf4436ff78404ad38b78d871bdd2b81d18d335044bb6ba8789ba0eb93e66cfd8;
  full-log12204613189 SHA07b3588f4a595ec68596dca0656aa1c77d806611a6767c3015785aa11ff642b8
  listed but not downloaded this phase. Browser success screenshot ci-success.jpg.
- Hash-bound complete linked ISA audit by skill-required independent agent
  /root/ace_kernel_isa DONE. Four instructionsections9082624bytes scanned;
  20default-v-A55 decode differences ALL embeddeddata.451unknownwords classified
  as tables/strings/twoexplicitdebuggertraps/onetrailingpadding. No actual
  STLUR/LDAPUR/PAC execution instruction identified. Four S3_5_C15_C2_6 accesses
  belong to Apple watchdog paths guarded by awl-scratch-supported; not proof
  of normalAcepathincompatibility. Raw evidence isa/audit.json +disassemblies.
  Static scan DOES NOT certify hardwareboot or complete runtime compatibility.
- Actual linked entry __startfffffe000749e488 branches start_first_cpu
  fffffe00074a00ec; LLVM sequence verifies x0BootArgs, offsets8/16/24/720,
  and no fixedRedmiFB writes in checkedentry. Saved entry-contract.json.
- Actual Ace kernel + candidate-3gADT now host-payload/ace.payload16933500bytes,
  SHA31ff937e6e3d416dc001d15e151b23a0c9d9ecd9f447e9f9f5f90e78450bb405.
  10segments,75766already-linkedlocalpointers validated. Actual C materialize
  returned0 usinglazy3GiBhostmapping and52realexcludedranges; EVERYsegmentfile
  byte matches MachO,966656BSSbytes clearedfroma5, ADT+736BBootArgs+pagepadding
  checked. Evidence materialize-verification.json and verify-materialize.py.
  No CPUjump/hardwareRAMwrite/phonecommand. Hostpayload is NOT Androidboot.img.
- REA exactkernel Ghidra12.1.4 import/analysis timedout at330000ms; cell765
  drained, rawprovidererror saved rea-entry.json. No REA function result was
  produced: export rea-evidence.json has0records, close snapshot0primitive/
  0workflow/0evidence; session CLOSED, no liveproviderrequest. Do not claim REA
  decompilation succeeded. LLVMfullISA and entryevidence independently complete.
  Retrying identical defaulttimeout is unjustified; largeranalysisbudget or
  cheaperanalyzerprofile requires scopedplan, notreinstalling existingprovider.
- Milestone15b1184 records actualkernel/payload/docs. This follow-up records
  REAtimeout/cleanup; no executable source change since171testsPASS. Final
  gitdiffcheckPASS. No newbuild/devicecommand/flash in this audit phase.
- NEXT real blocker: native phone loader runtimeFDT/MPIDR/ownershipchecks and
  earliestXNUtrace,16Kbootstrap. ace/xnu-loader is QEMU-only fixed-address
  harness and MUST NOT deploy. No storage/display/touch driver completed, no
  iOSuserspaceboot, no deployableiOS. No newflash/rebootauthorization used;
  originalboot_brestoration remains separatelypending. KeepgoalACTIVE.

## Earlier handoff (2026-10-20): Ace ADT + personal-fork full CI submitted

- Patch0086/source regression/docs committed7e9875e. Full171testsPASS30.870s.
  Forkbranchhead5ea487d7f403efb8739115550098bd568c7069b3 adds0086 toprior
  logfix0d45ed8. ThirdACE manualrun39288876908/job118183995118 is LIVE,
  latestBuildin_progress, allsetup/depsPASS, noartifacts yet. Thisrun MUSTbe
  inspected beforeanotherbuild; it is the firstfullattemptwithBearSSLfix.
  https://github.com/UnrealXu/ios-sweet/actions/runs/39288876908
  Goal-turn classification SOURCE + ACTUALfailedCIrootcausefixed + verifiedwait.
- Read-only USB check now confirmsdeviceonline, Androidsys.boot_completed1,
  SELinuxEnforcing. No reboot/rootrequest/newpartitionwrite. Captureprivate
  ace-ci-second-20261020/phone-health.json. Originalboot_b restoration still
  separatelypending, not authorizedbygoalcontinuation. Keep goalACTIVE.
- Preparednextartifactaudit: REAskill/nativeguide read, but no newREA target
  opened yet (thirdkernelnotavailable). Need linkedACEkernelprovenance+ISA
  audit; prebuiltSDKdependencies mayhave ISA beyondA55. EarlierSTLURrealphone
  SIGILL evidence remainsbinding. No hosttest/count proves iOShardwareboot.
- DIAGNOSIS RESOLVED from secondCI39287049187: job118176747089 COMPLETED/
  FAILURE, actualunfiltered122742lines recovered via independentlogartifact
  12203163315, zipSHA3010c9fb20f0f34b459a0b51aba2c71891327858335b2841143fd27a313a011a.
  Fourteen BearSSLunits fatalinner.hmissing, allremainingmakefailurescascade;
  no kernel/linkresult. Rawlog/privateerrors-context inace-ci-second-20261020.
  libkern/conf/Makefile.template softwareproviderflags remainedSWEET-only
  although source-staging alreadyacceptedACE. Patch0086 fixesTHISgate for
  headerpaths AND general-regs-only; unrelatedVMAPPLEstillnone. No MTKdriver.
- LOCAL verification: reproduceoriginalinner.hfailure usingrealfirstCIACE
  flags/headers. GNUmake expandsactualpatchedtemplateper-objectflags; all19
  providerMachOobjectsPASS. Addedmakepolicyregression(SWEET/ACE/VMAPPLE)PASS;
  full171testsPASS (exactruntimeinprivatefull-tests.log). Earliernewtestexpected
  19INCFLAGS entries butactual18+coreAESonlyCFLAGS; correctedtestinventory and
  reran. No hardwareexecution/phonecommand/flash. e753e8c committedCIlogfix/
  manualtoolchainprobe; patch0086+test/docs readyfornextsourcecommit/fullCI.
- NEW authoritative CI evidence: firstjob118161688122 check-run COMPLETED/
  FAILURE at16:15:41UTC, Buildexit2 (6m6s), total6m37s. Run-level API/UI lagged
  asQUEUED/in_progress during official GitHub Actions incident8tzbpcnl75jp;
  do NOT keep treating firstjob as live/blocked solelybyqueuedmetadata.
  No kernel in kernelartifact12202397569 (ziphash37415287...fff2b49), only
  support-library metadata. Buildtree12202735469 verified zipSHA
  02198a2301fc968de05a5375826b87a66b46f04ea9157ea6938460c0ab409d47,
  extractedprivately research/ace-ci-first-20261020/tree. ActualFLAGSselect
  ACE+cortex-a55. Do not call build failure causedbyincident: rooterrorunknown.
- Originaljoblog plugin twiceTransportclosed; web logtruncatedfirst~28k of
  122741 lines. Searchonlysaw11earlyoptionalpatcherrors, NOT actualfailure.
  Rawlink/download timedout; unsupportedcheckannotationsAPI tool and public
  anonymousAPIrate-limit preventedalternateannotations (summaryonlyexit2).
  Savedactualartifacts/inventory; no unsafecredential/browserstate extraction.
- FIXED CI diagnostics: workflowtee retainsfull xnu-build.log and filter
  tools/ci-build-output.py shows errors/context; pipefail preservesbuildexit.
  Independent xnu-build-log artifact alwaysuploaded. Bash/YAMLsyntaxPASS;
  samplepipeline preservesexit23. No kernelABI/sourcechange inthisretry.
  Forkbranch now0d45ed818cd23adc2bb6e2388db9876822f1e0d5, secondACE manual
  run39287049187/job118176747089 submitted; lastobservedQUEUED. Inspect this
  run's independentlogartifact; no reason to resubmit thirdcopy beforedata.
- Supportedrunnerprobe COMPLETED SUCCESS: run39285310958/job118169450577,
  forkmaincommiteeb1a86a2577353f4b5bb8b417629f44e011c6a0 addsONLYmanual
  .github/workflows/ace-toolchain-probe.yml (notkernelpatches). macos15-intel
  actual15.7.9/Xcode16.4; allavailableXcodes16/26, no15. iig--help has
  --deployment-target, but legacyIORPCcompatibility NOT tested/proven.
  Do NOT changeIORPCABI toforcecompile. Rawprobe log/statusAPIjson private
  research/ace-toolchain-20261020. CLIgh stillunauth; pluginwrites/browserdispatch.
- ActualfirstCI generatedheaders/flags replay: 23configuredARM64assembly
  units compiled torealMachO;22PASS includingstart/locore/caches/cswitch.
  SHA256unit failslocalclang18 onAppleq-registerSHAaliases; SAMEfailurewith
  previouslysuccessful SWEETbaseline. ThusnotidentifiedasAceCIrootcause;
  no kernelsourcepatch made for this localcompilerdifference. Rawobjects/
  stderr/replayJSONprivate ace-ci-first-20261020. No newphone operation.
- Latest goal-turn classification: SOURCE progress + VERIFIED WAIT. Added
  implementation/docs/tests committed219559b; worktree checkedclean afterward.
  tools/ace-mkpayload.py, bounded Mach-O/ADT to ACEXNU01 native-loader bundle;
  hostonly/no phone operation. Checks architecture/command/segment/entry,
  manifestADT/RAM/exclusions, exact filetails, allocation bounds and exclusive
  output. Rejects unresolved/dyld/chained/auth/threaded formats pending actual
  support. Does NOT create a boot.img or certify kernel platform/ownership.
- REAL cached SWEET format-control finding: no chained-fixups LC, but77056
  LC_DYSYMTAB local UNSIGNED records. Already contain plain linked pointers;
  zero virtualslide retains bytes (physical relocation isn't virtualslide).
  Initial parser over-refused all localtables; fixed to validate records,
  file-backed disjoint sites, targets and retained LINKEDIT. NOT an Ace image.
  Every loaded filebyte compared; actual ace_xnu_prepare returns0 and exact
  entry/ADT/args/top agreement for3GiBpolicy. No materialization/jump/phoneboot.
  Private research/ace-payload-20261020/verification.json and clearly named
  SWEET-format-control-NOT-DEPLOYABLE.payload. Local7newtestsPASS; full170tests
  PASS32.573s; docs/ACE-XNU-PAYLOAD.zh-CN.md. Initial threaded-refusal test
  setup changed unchangedfield; corrected sectionname and reran7/full170.
- Specific CI run39283161766/job118161688122 revalidated via plugin:QUEUED,
  no steps/logs/conclusion yet. Do NOT resubmit just because observationwaits.
  macos14brownout condition below persists; firstkernelbuild stillunavailable.
  Future actual ACE artifact must pass provenance/finalISA/packing audit.
  Current test kernel is SWEET and must NEVER be put in an Ace boot image.
- Implementation/docs/tests committed8e5cbf0; finalgitdiffcheckPASS. Current
  liveCI run39283161766 remainsQUEUED (no logs/steps yet), job118161688122.
  Official runner-images issue13518 confirms macos14brownout Oct19 14:00UTC
  throughOct20 00:00UTC (08:00China); checkedcurrent16:12UTC fallsinside.
  Brownout may affectqueue/failures; don't classify asXNUcompilefailure.
  Existingworkflow intentionallyneedsXcode15 iig ABI; blindlymovingtoXcode16
  changesIORPCkernelContentABI. Do not addguessedfield merelytoforcecompile.
  User GH-questionanswered: forkneedsno upstreamwrite. Personalpluginpush
  confirmedworking; no login/credential questionneeded forcurrentworkflow.
  Screenshot private ace-adt-20261019/ci-started.jpg; browsermarkedhandoff.
- New HOST/source milestone: tools/ace-mkadt.py creates bounded Ace CPU0 ADT
  from actual FDT, explicit cold-native RAM/source/stack policy; no phone RAM
  write. Excludes FDT/initrd/fixed reserves/bounded dynamic domains. Only two
  exact known Linux SSMR/SSHEAP CMA pools may remain uninstantiated before
  Linux; pinned OnePlus source supports Linux allocation semantics, not TEE
  ownership proof. Unknown unbounded pools/refused malformed ranges reject.
- Preferred private candidate candidate-3g: 2652B ADT, RAM140000000+c0000000,
  52 exclusions. Actual FDT SHA68c811fb...8560b. Root-readonly Android iomem
  classifies whole5..8GiB as System RAM, NOT free/exclusive memory. No new
  reset/MMIO/SMC/partition write. hardware_ram_ownership_verified=false.
- Patch0085 validates13MHz against CNTFRQ and handles absent bus clock with
  0/1 ratios, preventing divide by zero without invented frequency. Actual
  XNU SecureDT + clock source accepts live candidate on HOST; native C loader
  plan BootArgs agrees for1/3GiB windows using4-byteNOPfixture only. No jump.
  3 actual arm64 Mach-O clock compiles PASS; final163testsPASS69.249s.
  Evidence research/ace-adt-20261019/verification.json, sources/objects/logs.
  Documentation docs/ACE-XNU-ADT.zh-CN.md. XNU/iOS hardware boot remains absent.
- IMPORTANT correction to old GH blocker: logged-in browser AND GitHub plugin
  are UnrealXu. Upstream dipa-studio repo pull-only does NOT require upstream
  write rights: created personal fork UnrealXu/ios-sweet (push/admin true).
  User now explicitly approves using their GitHub plugin/account/fork CI.
  CLI gh still unauthenticated; plugin source writes + browser dispatch used.
- Fork minimal branch codex/ace-initial-platform, commit
  03be91534408e3fe39687841d602b6a79176925b, upstreambasefdad0de. Contains ONLY
  patches0082..0085 +3dependency stage scripts, no private research/NOTES or
  device IDs/Apple artifacts. Actions enabled, manual ACE/DEVELOPMENT/13.5
  full build submitted run39283161766, job118161688122; observedQUEUED.
  https://github.com/UnrealXu/ios-sweet/actions/runs/39283161766
  This is a LIVE CI job; inspect progress/results rather than submitting again.
- Current phone still has the ONCE-authorized diagnostic boot_b e2d7475e...
  pending originalboot_b restoration confirmation remains separate. Latest
  replayed approval is the already-executed diagnosticwrite, not anotherwrite.
  No fulllinkedACEkernel/newdeviceimage yet; no MTKstorage/display/touch/iOS.
  Next: inspect CI/full link + finalISA, earliesttrace/runtimeownership, then
  concrete separately confirmed physicalimage test. Keep goal ACTIVE.

## ACTIVE GOAL/handoff (2026-10-19): actual Ace iOS + physical-entry diagnostic candidate

- Latest implementation milestone committed c0553e1. Prior turn classification:
  REAL CPU0 ISA evidence plus XNU source progress. All local compiler/test
  sessions completed; no new live CI/REA/QEMU/device writer to wait on. Both
  pending human questions are information/authorization waits, not live jobs.

- NEW REAL PHONE finding + source fix: local Darwin clang18 retained implicit
  apple-m1 despite -marchv8.2+crypto. New pmsg core emitted STLUR(LRCPC2).
  Current PGKM10 cpuinfo advertises atomics/lrcpc but NOT ilrcpc. Built own
  static EL0 probe, taskset1/CPU0/getcpu checked; exact test-PC positive-code
  SIGILL caught, exit3. UID2000 shell, no root requested for execution; staged
  file removed, same Android/Enforcing/boot ID. Source diagnostics/ace-isa-probe;
  binary SHA13643257143b8ba20070f8146aa771bf2dabda8cf80cf1fa542b2d8b527093f8.
  Actual captures/journal research/ace-xnu-pmsg-20261019/isa-phone. This is EL0
  ISA verification only, NOT XNU/iOS execution. No reset/module/MMIO/SMC/flash.
- 0084 now explicitly adds -mcpu=cortex-a55 to ACE machine flags. Preserved
  pre-cpu-pin-core.o/asm as obsolete evidence; earlier implicit-M1 local ACE
  objects are NOT deployment artifacts. Current boot_b diagnostic is unrelated
  GNU assembly + unchanged OEM kernel and was not modified. Recompiled22 real
  platform Mach-O objects with A55; all PASS/no STLUR in checked objects. New
  core has NO undefined libc/atomic-runtime imports. Final10serial compiles
  alsoPASS; two SWEET control objects byte-identical to baseline. Actual
  genassym.c produces136constants matching cached offsets for A55 and SWEET.
  Full final151host tests PASS28.486s. No full linked ACE kernel/CI run yet.
- 0084 also adds real XNU pmsg serial backend at normal KPRINTF startup.
  Explicit ace_pmsg=1 plus exact ADT /chosen/ace-pmsg compatible/reg/ECC/type
  required; BootArgsrev2/ver2, EL1/LE and pmsg outside managed RAM checked.
  Only pinned48160000+10000 resource requested via ml_io_map_wcomb (4aligned
  16Kpages); no32MiBmapping/unknown-zone init. Core retains valid DBGC ring,
  validates each char, nonblocking normal-RAM lock drops recursion/contention,
  ordered data/header + platform DSB. Not crash-transactional/retention proof.
  Backend has NOT executed on phone; pre-MMU/first-C logging remains missing.
- Tests execute the SAME patched C core/frontend; host adapter replaces CPU
  registers, mapping and DSB, NOT hardware.19policy-refusal cases, malformed
  maps/headers, old/wrapped data, recursion and400header variants PASS. ASan+
  UBSan/guard pages3wraps+1024statesPASS. Actual A55 flag/ISA/no-import regression
  PASS. Raw sigaction UAPI ABI assertions PASS against actual cached Android
  declarations (private compiler implementation skipped; declarations intact).
  Initial UAPI include setup failed; successful ABI compile occurred AFTER
  the one phone probe. Exact-PC runtime signal check independently succeeded.
- Final root-readonly phone hash/health PASS: diagnostic boot_b e2d7475e...
  and vendor_boot bb5a094d... match pins, same boot ID/Android1/Enforcing.
  No new partition write. Both pending questions remain unanswered: original
  boot_b restore authorization and GH login/write access. gh rechecked still
  unauthenticated. No retry of diagnostic flash or ISA probe. Goal ACTIVE.
- Source/evidence details: docs/ACE-XNU-PMSG.zh-CN.md; private verification.json,
  compiled objects, source/capture hashes, logs in ace-xnu-pmsg-20261019.
  Next mainline: Ace ADT/loader memory ownership, earliest boot trace, full
  ACE build/link and final library ISA audit, then a concrete separately
  confirmed device image. MTK storage/display/touch remain UNFINISHED.

- Pending new async information request: complete gh auth login with repository
  write access; local ACE source is concrete/committed. No response yet. This
  is separate from pending boot_b restore confirmation. Continue independent
  host work; do not infer either reply from automatic goal continuation.
- Re-audited byte-pinned live FDT: one RAM bank40000000+200000000,51reserved
  nodes,3dynamic; vcp_share has bounded alloc-ranges but ssmr/ssheap CMA lack
  alloc-ranges. So absent fixed-reg overlap in5..6GiB is NOT exclusive RAM
  proof. Initial actual Android dmesg has CMA239000000+6000000 and
  23f800000+400000; only that Android allocation, NOT next cold-boot ownership.
  Private live-fdt-memory.json/android-cma-corroboration.json retain source
  hash/scope. No XNU RAM default selected, and no device operation occurred.

- ACE source milestone committed d993e6a. Patch clean dry-run applies to the
  0082 baseline. No CI or phone operation. Initial cached diff whitespace check
  flagged mandatory unified-patch context prefixes, not generated source
  whitespace; .gitattributes now treats patch files as patch data. Source,
  tests and scripts retain normal whitespace checks. Pending GH access setup
  and separately pending original boot_b restoration remain unapproved.

- Latest SOURCE milestone: patch0083 adds MACHINE_CONFIG=ACE, ACE.h and
  MASTER.arm64.ace. Retains ARM64_BOARD_CONFIG_SWEET as shared OSS software
  compatibility selector; ACE board selection takes precedence. MAX_CPUS1,
  SMP limit1, PPI27, earlyfb0. Explicitly excludes6Qualcomm MMIO C drivers,
  Battery/Framebuffer, UFS root/log callers and later fbcon; ACE registry adds
  only platform expert + bootCPU. This is NOT a linked/bootable Ace kernel.
- Fixed all3dependency staging scripts (pthread/BearSSL/HFS) to accept ACE,
  otherwise fresh CI would lack sources that happen to exist in local cache.
  Actual21files x baseline/SWEET/ACE=63 Mach-O compiles PASS. After common
  file-prefix mapping, all21SWEET objects byte-identical to baseline. ACE9
  implementation units have no global symbols;5caller units have no residual
  UFS/log/earlyfb refs. Actual genassym.c compiled to assembly in both target
  configs:136constants each exactly equal cached assym.s. This covers tested
  offsets, not complete ACE config regeneration/full link or hardware MMU.
- 5new regression cases PASS: actualACEheaderABI/framebuffer override refusal,
  QCOM/Battery emptyobjects, honestACE registry, and dependency stage gates.
  Final full141tests PASS27.813s; full-tests-final.log. git diff --check PASS.
  Private research/ace-xnu-platform-20261019 contains compile.py, objects,
  compile-final.log,verification.json,genassym.py/results,CI access evidence.
  Initial C++ replay omitted CFLAGS (CXXFLAGS only adds language flags), fixed
  to follow actual P_RULE_1A and reran all63. Original caches untouched.
- Full CI external condition revalidated: gh unauthenticated; GitHub connector
  get_repo reports pull=true,push=false for dipa-studio/ios-sweet. NO remote
  write attempted/new run. Do not claim build/boot. Need authenticated write
  access for a branch CI run; host ADT/log/memory/controller work can proceed.
  No phone command, reboot, flash, module/MMIO/DMA operation this turn.
  Original boot_b restore authorization still pending, NOT approved by goal
  continuation or original diagnostic-write answer. Keep goal ACTIVE.

- Console isolation milestone committed as7e04f6a; patch clean dry-run
  applies to unchanged cached baseline. No CI push or phone write.
- Latest continuation: previous turn was REAL hardware-entry progress; this
  turn made SOURCE progress, not a new hardware boot. Added patch0082 to
  separate fixed Redmi early framebuffer from generic SWEET ARM/GIC paths.
  SWEET_HAS_EARLY_FB defaults1; explicit0 removes stage0 writes, bootstrap
  and final32MiB framebuffer mappings, early C console; inline no-ops avoid
  unresolved caller references. DOES NOT create Ace target or disable later
  Qualcomm drivers/ADT fbcon; no new logging backend or phone deployment.
- Actual cached CI39158169212 flags/headers replayed with Linux clang18:
  5files x baseline/default/disabled=15 real arm64 Mach-O compiles PASS.
  All5 default objects byte-identical to baseline; all5 disabled objects
  have no sweet_early symbol/reference (llvm-nm). Initially stale exported
  header copies invalidated local default check; BOTH EXPORT_HDRS refreshed
  from edited source and final15compiles rerun. Original cache untouched.
  Private research/ace-xnu-console-20261019 contains compile.py, objects,
  compile-final.log, verification.json. Full136tests PASS26.347s. No new
  full-kernel CI/link/build: gh unauthenticated, connector old-log download
  Transport closed; used actual stored .CFLAGS/.SFLAGS instead. See
  docs/ACE-XNU-BOOTSTRAP.zh-CN.md for implementation and exact limits.
- Read-only USB phone health PASS this turn: Android/root/Enforcing, same
  diagnostic boot_b e2d7475e... and unchanged vendor_boot bb5a094d....
  No new reboot, partition write, module load, MMIO or DMA. Pending restore
  question still unanswered; the newly replayed user answer authorizes ONLY
  the diagnostic write ALREADY executed, not restoration or another flash.
  Goal remains ACTIVE; genuine XNU/iOS hardware boot still absent.

- Pending async user question requests ONLY exact original boot_b restoration
  (ee817627...d0deed10,64MiB) + reboot/hash/health verification. NO reply yet
  as of this handoff. Do NOT restore until human answer. Goal remains ACTIVE.
  Hardware entry/log milestone commit86ec0f2, authorized-flash journal554deee,
  initial Android/no-marker09bbf15, candidate source852513b, parser/auth8dc7b75.
- While waiting, read actual live FDT from the observed handoff boot (x0
  47c80000). Private driver-handoff/live-fdt-after-prefix.dtb SHA
  68c811fbaae657372d740c25ff81f03c9763eab3e897b0a7104d624ec598560b.
  Chosen separate BE fields corroborate LK fbbasefe1af000/VRAM1e50000,
  matching mblock-14-framebuffer. 16K mapping would round tofe1ac000..
  100000000 with0x3000offset, requiring extra padding ownership NOT yet
  established. Boot pitch/format/current DMA scanout remain UNKNOWN. Actual
  UFS node112b0000,size2300 uses legacy mt8183-ufshci compatible on this
  MT6895; don't infer SoC identity from compatible or use guessed11270000.
  Metadata only; no framebuffer/MMIO write. Selected/decoded JSON private.
- CRITICAL NEW HARDWARE MILESTONE: ordinary Android reboot2 RETRIEVED exact
  unique pmsg token + full80B prefix record! Actual incomingEL1, x0/FDT
  47c80000, SCTLR30d00800(M/C/EEoff),MIDR412fd050,MMFR0101122,CNTFRQ13MHz,
  logger0,stock_entry40200000. Raw pmsg439B,recordoffset359. Android ready,
  new bootID, boot_b candidate/vendor_boot hashes unchanged. result-verified
  and captures in phone-test1/normal-reboot2. This is REAL custom entry and
  log retrieval, NOT XNU/iOS. First fastboot reboot had NO log; cause remains
  UNDETERMINED, do not assert LK cleared RAM or extrapolate EL2 behavior.
  Current physical phone still has candidate boot_b, NOT restored. No second
  raw partition write yet. Next request is exact original boot_b restoration,
  which is NOT covered by first-step authorization.
- Deferred fixed-prefix-RAM readonly module prototype was NEVER loaded on
  phone/QEMU. Host build initially lacked authentic stack/memset CRCs; added
  6authentic imports, module-v2 built135776B bf812106...7a. Since pstore now
  worked, removed unneeded active diagnostics/ace-chain-record source and
  preserved privately in research/ace-chain-record-20261019/deferred-host-only-source.
  No arbitrary RAM read was performed. Do not revive unless a concrete need.
- INITIAL OBSERVATION (superseded by reboot2 log above): diagnostic booted Android, root/Enforcing/
  Bslot/boot1, actual boot_b SHA equals candidate e2d7475e...1ed834d;
  vendor_boot SHA unchanged, boot ID changed, Kernel code moved40000000 ->
  40200000 exactly as stock payload offset. pstore pmsg62B has NO current
  token; prefix register record NOT verified. Do not invent EL/log success.
  Phone is running diagnostic boot_b, backup NOT restored/authorized. Continue
  exact backup restoration after individual confirmation; logs now retrieved.
  Actual result/journal research/ace-stock-chain-20261019/phone-test1/
  result.json/state.json. No further partition write is authorized.
- LIVE DEVICE STATE: USER-authorized exact diagnostic boot_b flash EXECUTED
  ONCE. Sending65536KB OKAY1.379s; Writingboot_b OKAY0.140s; rc0/1.522s.
  Candidate SHAe2d7475e...1ed834d now written. Normal fastboot reboot sent;
  Android/pstore observation completed as above. Private execution journal is
  research/ace-stock-chain-20261019/phone-test1/state.json, flash-boot-b.log,
  transport.json and reboot-and-observe.py. DO NOT flash again or assume
  backup restored. Restore NOT authorized yet. Only boot_b was written.
  Initial partition-size guard rejected hex without0x; rechecked parsebase16,
  exact67108864 confirmed before write. Device USB identity equals ADB ID.
- USER EXPLICITLY REQUESTED persistent goal: run genuine iOS on their PGKM10
  and make it normally usable; use REAL phone verification, not simulation
  as substitute. create_goal succeeded, status ACTIVE, no token budget. Keep
  goal active; no XNU/iOS hardware boot yet, so DO NOT mark complete. Boot logo,
  Android launcher, diagnostic module/QEMU/synthetic receiver are insufficient.
- Mainline is now real custom-entry proof. Two actual ADB transports(USB/TLS)
  authorized; root/Enforcing/Bslot/boot1. Actual vendor_boot_b SHA matches
  pinned backup. Read-only live kernel layout/lock evidence saved privately:
  Kernel code40000000, initrd66f00000..69509a70, unlocked/orange/flash_locked0.
- Actual USB normal adb reboot bootloader -> getvar only -> fastboot reboot
  -> Android PASS. productk6895v1_64/slotb/unlockedyes/nonuserspace/max4000000.
  Boot ID changed; actual boot_b/vendor_boot_b hashes unchanged, Android
  root/Enforcing/boot1. NO flash/erase/set_active/SMC/partition write. Before
  reboot saved old pstore. Evidence research/ace-goal-device-20261019/
  usb-roundtrip/result.json. Manual key bootloader entry/restore flash UNTESTED.
- Extracted CURRENT byte-matched vendor_boot_b actual recovery/fastbootd/HAL,
 929CPIO entries. REA closed snapshots rea-mtk-fastboot-hal.json(2records) and
  rea-fastbootd.json(3records). Constructor18handlers has no boot/continue;
  dispatcher map miss fails, download onlyreceives. OEM handler calls HAL
  (plus directly rejected postwipedata special case); extracted MTK HAL
  doOemCommand alwaysstatus3 unsupported. EIDs/details in new plan doc.
  This corrects earlier AOSP-only scope; does NOT rule out every firmware
  private path or prove actual runtime HAL binding. No OEM command executed.
- New ace/stock-chain: small diagnostic prefix -> unchanged full original
  Android kernel offset2MiB. Original text_offset0/flags0xa preserved. No
  stack/MSR/EL-switch/SMC/GIC/DMA/reset/storage operation. x0..x3/LR restored.
  Optional explicit pmsg guard excludes ENTIRE large Image, then reuses
  unchanged pmsg.S canonical/control/LE checks. Unique token +80byte register
  record append; failure continues stock without initializing unknown RAM.
- SIX actual QEMU cases all booted real exact stock kernel through normal
  module load/unload and poweroff: plainEL2,pmsgEL1/EL2,relocation,bad-header,
  full-image-alias refusal. Full49185772B runtime kernel hash checked each;
  exact handoff registers/ring/raw record. This was preflight; subsequent Ace
  hardware candidate execution is recorded above. Current report research/ace-stock-chain-20261019/verification.json SHA
  3edd4c4760b84aa039f90b01468970d47c7755874106c3af439082e1b2561227;
  root independently checked5source/54artifact hashes. All QEMU exited.
- tools/ace-stock-chain-boot.py binds6cases/raw/source hashes, current Magisk
  backup pin, gzip/extraction/header/ramdisk/kernel identity. IMPORTANT found
  and fixed short bare-flash stale-AVB-footer risk BEFORE any phone write.
  Current Magisk and original AVB metadata1600B are byte-identical, SHA
  c80565ce5c50d72aecf13bf253071213974c76df6f9fbf9c99a9cda2a68bb16c;
  actual modified ramdisk and footer offsets differ. Final candidate follows
  observed Magisk layout: preserve obsolete metadata bytes, relocate them,
  update footer geometry and fill ENTIRE64MiB; NO authentication claim.
- ONLY final candidate: research/ace-stock-chain-20261019/final-review-candidate/
  diagnostic-boot-b.img,67108864B, SHA
  e2d7475e99d3449e7dbcf16e473a65a27a8f3ceae19278744ae32b3601ed834d.
  Marker f283070db2b9aa1092d13ca9. Keeps exact current Magisk ramdisk SHA
  54961de2dad343c35295905f1f1811b80d176e725b9fa93c48aada8e96fa90d2.
  Earlier review-candidate BARE image is obsolete/NEVER deploy. Current
  candidate not authenticated or iOS. LK acceptance and ordinary-reboot log
  retrieval now observed above; full cache ownership/manual restore unverified.
- Actual boot_b rollback backup67108864B SHAee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10
  in research/ace-backup-20261019-wireless-v2. Do not modify vendor_boot,
  vbmeta,GPT,userdata,bootloader,recovery,modem,persist or slot. Detailed
  concrete plan docs/ACE-STOCK-CHAIN-PLAN.zh-CN.md. Per AGENTS each specific
  destructive write needs individual confirmation, including restoration.
  USER NOW explicitly approved THIS e2d7475e...1ed834d boot_b write and
  confirmed present for manual recovery (async answer: 同意本次写入，我在手机旁可协助恢复).
  Authorization covers this one diagnostic write, NOT backup restoration.
  Do not repeat a write after an unknown outcome; inspect private execution
  state and actual boot hash first. Execution preflight starts next.
- Six new packaging/guard tests PASS; final full133tests PASS26.889s,
  full-tests-final.log; earlier133tests before AVB correction also PASS26.757s
  and retained. Final candidate independently rehashed. git diff --check PASS.
  No new CI/fullXNU build/push. REA sessions closed; no device writer remains.
- NEXT: flash already done; observe current reboot and independently verify
  captured successful hardware record. Obtain separate confirmation before
  exact backup restoration, then execute/verify actual restore. Then pursue Ace
  XNU/ADT/16K/GIC/SMP and MTK controllers; all still unfinished.

## Previous milestone (2026-10-19): Ace XNU flat-segment loader/BootArgs foundation

- User asks to continue custom entry/XNU/MTK fixes. Implemented bounded,
  independently tested loading/BootArgs component; actual LK custom entry,
  full Ace XNU platform and MTK UFS/DSI/touch controllers remain UNFINISHED.
  No ADB, reboot, device RAM/module/MMIO/SMC/partition operation this turn.
  No deployable Ace iOS image or actual XNU execution is claimed.
- New ace/xnu_handoff.c/.h: explicit RAM/source/reserved policy, distinct
  ACEXNU01/v1 flat PRE-REBASED bundle (reject SWEETXNU);1..32segments;
  bounds/overflow/table/source/ADT/destination overlaps and entry-in-BSS/gap
  checks before any target write. Exact byte copies and BSS tails, no rounded
  source reads or overrun. Entire XNU RAM window must exclude reservations,
  not just copied segments. Host/mapped metadata/source aliases refused.
- Builds XNU8796 Revision2/Version2 BootArgs736B, ADT VA vs physical incoming
  x0/entry/top semantics; video disabled because Ace framebuffer PA unknown.
  ADT is OPAQUE copied input, not a generated/validated Ace platform tree.
  No Mach-O/IMG4 parser/rebaser, MMU tables, XNU machine target, SMP/controller
  support or phone address default. Caller must establish RAM ownership and
  honest physical mapping/policy; source/policy cannot mutate concurrently.
- Existing Qualcomm shim/loader.c has fixed sweet FB and insufficient bounds/
  rounded-copy assumptions; new Ace code is isolated. Original sweet and
  ace/entry32case baseline sources/artifacts remain unchanged.
- New ace/xnu-loader QEMU-only harness actually executes SAME C loader,
  cache synchronization and branch to SYNTHETIC receiver (NOT XNU). Five
  actual cases PASS: EL1,EL2->EL1,relocatedEL2; entry-in-BSS/overlap refuse.
  Whole256KiB target RAM compared for all5, including precise13-byte tails,
  BSS/gaps/ADT/all BootArgs, and complete unchanged target on refusals.
  Receiver independently records x0..x3,CurrentEL,SCTLR,DT VA/top. Explicit
  QEMU RAM41000000/40000 only; never use this harness as Ace deployment.
- Private research/ace-xnu-handoff-20261019/verification.json SHA
  dfda0938047e89753428c226f13952b539c5dbd7207e775bee14b41e6f939134.
  Root independently recomputed8source/72artifact hashes;
  independent-review.json retains provenance and no-hardware/no-iOS flags.
  Early assembler immediate error and first fixture13-vs14byte literal
  comparison failure were fixed; prior whole-RAM failure log retained. These
  were development fixture failures, not observed phone/XNU kernel failures.
- Ten new host tests PASS, including ASan+UBSan5000 bounded mutations with
  target/output unchanged on refusal and ARM64 no undefined libc symbols.
  Full127tests PASS21.955s, private research/ace-xnu-handoff-full-tests.log.
  Actual cached XNU Boot_Video/boot_args declarations compiled to compare
  every ABI offset/size, not just our duplicated constants. boot.h SHA
  efdfec46319cb147297682a8faebe02873f845261b57f7511ab8e15c13ef3439,
  prior source CI39158169212; this optional test skips when artifact absent.
  No new full XNU build/gh run/push. git diff --check PASS.
- Loader/tests/documentation milestone committed as ce56f4c. All QEMU
  instances from this harness exited; no REA session was opened this turn.
- Next: establish real custom-code entry/recovery; build Ace ADT from proven
  memory ownership and platform facts, connect loader to real Ace XNU target;
  validate GIC/timer16K mappings then actual MTK controllers. Existing stock
  fastboot boot remains unsupported; do not repeat it or patch LK/preloader/
  guess OEM commands. No valid flash plan; destructive partition steps still
  require concrete candidate/rollback and individual user confirmation.

## Previous milestone (2026-10-19): GIC/timer QEMU IRQs + eight-core phone observations

- User requests continued fixes and iOS real-device validation. iOS still NOT
  bootable/deployable. This milestone is diagnostic; no partition write,
  reboot, bootloader command, SMC or flash. Android remains booted/root/
  Enforcing; normal temporary module was loaded/unloaded eight times below.
- Added independent ace/irq-probe single-CPU cold-boot QEMU-only Image. Five
  real cases PASS: EL1,EL2->EL1,relocatedEL2 each3PPI27 IRQs/3EOIs with actual
 62500000Hz and increasing per-IRQ timestamps; disabled timer bounded timeout;
  BRK exception EC3c recorded. Explicit QEMU GICD08000000/GICR080a0000 ONLY.
  Does NOT preserve live Linux state, implement SMP or run Ace addresses.
  Original ace/entry32cases/source/binary baseline unchanged.
- Private research/ace-irq-probe-20261019/verification.json SHA
  713d872f2c926f35d3f8a941d26d3722ec9e534ff6f555b0e447f7e9aa595e62;
  all5source/24artifact hashes independently checked. No iOS claim.
- New diagnostics/ace-irq-timer read-only architectural register probe normal
  Kbuild:8830exact headers/430scripts, two authentic OEM CRCs, original CFI/
  LTO/SCS/PAC/BTI retained; prepared Module.symvers restored. Module134816B SHA
  6e19e1b09c6d57d02131716b9c36fd458e495bd47fafd068660415737dc69398.
  Exact stock kernel QEMU normal load/unload PASS15.118s/poweroff/exit0.
  REA exact .ko init review ev_4abd9b6776711ada83514d1bb6f4dee418c21c9fbcdeae3c1da7c43d55c3c935;
  snapshot rea-module-snapshot.json saved/CLOSED(2records). No IAR reads/MSR/
  MMIO/timer programming; ordinary printk/SCS/tracing still write kernel RAM.
- REAL PHONE: normal insmod/rmmod pinned separately to all8online CPUs PASS.
  EL1/13MHz/CNTV_CTL1/ICC_SRE7/CTL8400/PMRf0/IGRPEN1=1/BPR1=3 throughout.
  MPIDR81000000..81000700: Aff1 varies, Aff0=0; do NOT assume Aff0=CPU index.
  Android IRQ line20 corresponds GIC INTID27, counts increased on all8cores
  by870,644,418,528,463,415,536,366 during measurement. These are Android
  driver observations, NOT baremetal interrupt delivery/SMP/PSCI tests.
- Evidence research/ace-irq-timer-live-20261019/phone-run1: same boot ID/taint,
  Enforcing/boot1, no residual module, staged file removed. Initial result.json
  FALSE retained: parser wrongly demanded adjacent reads strictly advance;
  3cores returned same13MHz tick legitimately. Corrected rule>=within sample,
  strict progression across CPU samples, backwards/stale/malformed rejected.
  result-verified.json revalidated SAME raw capture OFFLINE; no second run.
- profiles/ace-mt6895.json and diagnostics README record observed topology/
  register facts and limits. Root reviewed independent IRQ probe; qemu_baseline
  performed that subtask under already-active REA decomposition; no overlaps.
- Source/evidence milestone committed as ed48b01. Final read-only phone health
  PASS: same boot/boot1/Enforcing/no residual module or staged file; private
  final-health.txt. All REA sessions closed, all probe QEMU instances exited.
- Final117host tests PASS14.204s (private full-tests.log), including6new
  IRQ/observation boundaries; git diff --check PASS. Root independently
  rehashed5IRQcases/24artifacts/5sources and6phone captures/current parser.
  Phone verified report SHA368c284ae1a18fa5f8f3620731972565d447365300b5e41b2d0ea1f238cdeb78.
- Current hard blocker unchanged: verified custom-code entry and recovery,
  then XNU loader/ADT/BootArgs, real GIC/timer/SMP + MTK UFS/DSI/touch drivers.
  Standard fastboot boot unsupported; do not repeat/patch LK or guess OEM names.
  No new gh CI/full kernel build/push. No flashable iOS candidate exists;
  destructive writes still require concrete validated plan + per-step approval.

## Previous milestone (2026-10-19): entry investigation + optional logging/packaging verified

- User requests deeper fixes and flash iOS AFTER success. Conditional success
  is NOT met: diagnostic QEMU passes do not mean XNU/MTK/iOS works. No phone
  reboot, module load, RAM write, OEM/SMC command or partition operation this
  turn. Only final read-only ADB health check: PGKM10/MT6895/B/boot1/root/
  Enforcing/tls-ready PASS, private device-health-readonly.json. Existing USB
  and paired wireless authorization persists; do not ask pairing again.
- LK register/dispatcher/continue source-preserving analysis completed below,
  milestone commit fcd5584. Standard boot unknown is missing prefix handler,
  distinct from security/lock refusal. Continue signals storage boot thread,
  not download-RAM jump; known direct registration coverage14sites (13BL+
  tailB), two caller functions. Indirect/other-firmware paths NOT ruled out.
  Exact config KEXEC/KEXEC_FILE/CRASH_DUMP disabled; AOSP15 fastbootd has no
  boot/continue. OEM extensions/custom handoff remain UNVERIFIED.
- Added optional ace/entry/pmsg.S logger, explicit --pmsg-ram ADDRESS BYTES;
  DEFAULT remains byte-identical ff298998dfbc9b05a26904b095dabd90fb75f2293fa3abd31e6788d6ad965838.
  No hardware default address. Single-writer LE/ECC0/exclusive ordinary RAM
  prerequisite, rejects M/C on, invalid/noncanonical DBGC and runtime Image
  overlap; appends acceptedEL + payloadEL1 text, preserves old bytes until
  ring wrap, dsb sy. No unknown-header initialization, reset/SMC/MMIO/storage.
  This IS a RAM writer when enabled; NEVER confuse it with readonly module.
- 32 DISTINCT actual QEMU cases PASS: default4,43000000/128-byte ring14,
  and48160000/65536-byte ring/QEMU256MiB14. Wrap,EL1/EL2,relocation,bad
  signature/cursor/noncanonical,MMU-on refusal + image alias tested. Only
  simulated RAM, NOT actual physical pmsg writer/reset/ownership/cache test.
- Fixed stale-dump risk: unlink prior ring/table/status before case; preserve
  actual MMU trampoline among hash-bound artifacts. Fixed real hash timing
  bug: wait for QEMU termination before hashing logs (shutdown appends text).
  Two verifiers now explicitly refuse -O/PYTHONOPTIMIZE; cannot publish
  unchecked PASS when assert checks are disabled. Focused negative tests3
  PASS, final full111 unit tests PASS (final-clean run9.677s). git diff --check PASS.
- All7entry source hashes and281artifact hashes independently recomputed by
  root/packaging worker after final run. Final report SHA256:
  research/ace-entry-20261019/verification.json
  b84d6d15fcba189ae8b1f2ad5e212eec52d926627c05060caa14c7d45d336e1d;
  research/ace-entry-pmsg-20261019/verification.json
  db9621712e8f53912c78a5f71a65b6acc23d3222269a3b2874653031ac2bc24e;
  research/ace-entry-pmsg-ace-address-20261019/verification.json
  4cf6047021adbc53d46ba2f893b28c6def6568c7d12587b8e9bcb3ae4b922f32.
- Added tools/ace-entry-boot.py +14mutation/format tests. Reuses exact stock
  pins/strictv4/gzip; independently validates all source hashes, original
  probe8 raw records, default4 + dual14 cases/raw pmsg/page tables/log hashes.
  Default gzip only; explicit unsigned review flag and optional experimental
  Ace pmsg selector. No AVB/RSA claim, no transport/device operations.
- FORMAL current private wrappers: research/ace-entry-wrapper-20261019/
  final-clean-default,final-clean-unsigned,final-clean-pmsg. Independent
  roundtrip PASS in final-clean-independent-roundtrip.json; parent prior review
  research/ace-entry-options-20261019/wrapper-parent-review.json. Previous
  wrapper folders bind older verifier sources; keep as history, do not deploy.
  Both unsigned candidates1667072B; defaultSHA
  efcadb6bb4b2d87cba774f7970e0519bd91f14e484a8baa920069a08fa9b45eb;
  pmsgSHA26c4a3bfff694b5401644ec000d40f8a40ed380626eeb66ed2ed76221e31f456,
  embedded ImageSHA5a13311daf1d6b16b68e59454ce269af703e90bff42737ec390a8e3a25dddb74.
  All ios_deployable=false/hardware_test_recommended=false; no image sent to
  phone. Payload is ACEENTRY->ACEPROBE, NOT XNU/iOS. Defaults leave pmsg off.
- Entry logging/packaging source milestone committed as7963a70, after
  LK investigationfcd5584. Trailing EOF whitespace corrected afterward; formal
  final-clean wrappers rebuilt with the current tool hash, candidate bytes
  unchanged and independently re-extracted; source/records still fully bound.
- Final artifact/handoff/whitespace commit5b3161c; working tree clean.
- Host preflight PASS/no errors. No new full kernel/XNU build, gh CI run or
  push. All agent work finished; all REA sessions CLOSED (worker7records,
  nativeVA5records, snapshots private); no device writer/QEMU remains.
- Next actual prerequisites: verified custom-code entry and physical recovery
  route; ownership/cache/reset log retrieval; then XNU loader/ADT/BootArgs,
  GIC/timer/SMP and actual UFS/DSI/touch controllers. Full iOS remains
  UNFINISHED. Do not patch LK/preloader/GPT or try OEM debug names blindly.
  Bare diagnostic file is not a validated flash plan. Per AGENTS any eventual
  destructive write needs concrete candidate + rollback and per-step approval.

## Previous milestone (2026-10-19): continue/dispatch resolved; optional pmsg bridge preparation

- User explicitly requests deeper fixes and, after success, iOS flash/test.
  iOS remains UNFINISHED; no phone command, reboot, RAM write or partition
  operation in this milestone. Current artifact work is diagnostic, NOT iOS.
- Read full existing LK command-table/recovery reports before expanding; do
  not repeat standard fastboot boot test. Standard kexec/FILE/CRASH_DUMP are
  disabled in exact stock config;2895 enabled macros match actual headers.
  AOSP15 fastbootd has no boot/continue handler. Source evidence saved in
  research/ace-entry-options-20261019/{verification,source-manifest}.json.
- Solved Ghidra raw-entry coverage gap: source-identical suffix at6620 seeds
  worker; parent/slice hashes and explicit map recorded. Worker REA complete:
  ev_b97e1f90e8a6d0232a28cddd489a00895d09eea97fdd3805a2ff97f895c69904.
  continue6ea8 -> OKAY/stop/notify boot eventddc60; event waiterecac then
  threadec9c callsde78 (load_vfy_boot storage0/1), NOT a download-RAM jump.
  Raw worker snapshot CLOSED (7records), no physical placement claim.
- Added tools/ace-lk-analysis-elf.py: analysis-only ELF wraps exact parent
  bytes unchanged, native linker VA inferredffff000050f00000; e_paddr0,
  no invented BSS, analyst_*labels at independently decoded prologues.
  ParentSHA9e3f9fd5..., wrapperSHA3c60dfbdc337b6f94bf2c9d5b8b6aa08396e48c3a87cf74372514ded80c14c5a.
  NEVER deploy this container.3 focused structural/pin/byte-identity tests PASS.
- NativeVA REA dispatcher5f50 complete: prefix-list miss -> unknown command;
  security/lock refusal are distinct matched-handler paths. Evidence
  ev_0a066ca1cce0fc11f8af4c886d0d0d4537d7d7e1cabc2641dd6e0d9bc36b1ed6.
  Worker allocates64MiB, calls dispatcher, frees buffer on return; direct
  registration calls13BL+1tailB (14REA incoming) only worker/downloadregister.
  This does not cover all indirect registrations or alternate firmware paths.
  NativeVA continue/store path cross-checked; docs/ACE-ENTRY-OPTIONS.zh-CN.md
  holds evidence IDs and limits. rea-lk-nativeva-snapshot.json CLOSED(5records).
- REA skill explicitly decomposed independent work: ace_cpu_probe completed
  config/fastbootd sources; qemu_baseline implementing optional ace/entry RAM
  logger (default binary unchanged; explicit address/size; no unknown header
  init), pure QEMU only. mt6895_evidence preparing host-only diagnostic gzip/
  unsigned wrapper with strict source/raw-record evidence binding. They own
  ace/entry and tools/ace-entry-boot.py/tests respectively; do not overlap edits.
- Root will review final schemas/code and exact QEMU results, then commit
  completed source/docs/tests. Experimental logger not deployed. Next remains
  actual custom-code entry plus reset/retrieval, then XNU/controllers; no
  destructive fallback until concrete validated image/recovery/per-step approval.

## Previous milestone (2026-10-19): raw pmsg header PASS; fastboot boot UNSUPPORTED

- User said continue; persistent authorization for wireless connection retained.
  User connected USB when requested; actual Android USB CONFIGURED/online1,
  one USB ADB and one paired TLS transport. Do not ask pairing again.
- New diagnostics/ace-pmsg-header/ implements fixed0x48160000+12B header
  read through same WC mapping as actual ramoops mem_type0; 4KiB mapped page
  stays inside64KiB pmsg. Keeps tracing/CFI/LTO/SCS/PAC/BTI; no pmsg writes,
  init/zap/force-load or payload reads. printk/trace can write other normal
  kernel memory and the separate console log; do not claim zero RAM writes.
- Exact8830headers/430scripts verified.9 authentic CRCs all directly from
  pinned original mediatek-drm.ko5ae1377b...; no fake versions. Partial symvers
  class/namespace reference evidence in imports/imports-manifest.json SHA
  9d67d90f91dcbe1eb711270e3be4e41b258c9950a1aa93be8481c73e4be84e05.
  Source reference EXPORT_SYMBOL/GPL distinctions retained; original prepared
  tree Module.symvers restored. Not an original full OEM symbol table.
- FINAL module148184B SHA
  c15323b76d08c75921ee31601cf85de9788402e707e8517ad698c83fffeea5b4.
  research/ace-pmsg-header-20261019/module-live/build-result.json.
  Stock-kernel QEMU with actual no-map ramoops reservation:14.967s/exit0,
  normal load/unload twice; DBGC/start=size0 then normal pmsg-driver27-byte
  write and DBGC/start=size27/capacity65524. qemu-live-candidate/result.json.
  Earlier fixture failures(DTS ordering/proc-misc vs real pmsg chrdev/parser
  diagnostic build warning) retained; qemu-run5/old and qemu-final also PASS.
- REAL PHONE normal insmod/rmmod both0, direct sig43474244/start288/size288/
  capacity65524, stable first try, ECC0. Same boot ID/taint unchanged, boot1,
  root and Enforcing normal, no residual module and staged file removed.
  Saved previous pstore files first. Actual execution ONCE, no pmsg write.
  Initial live parser rejected ANSI-colored tag; fixed +4 regression tests,
  revalidated same saved capture OFFLINE without a second phone load.
  Evidence live-run1/result-verified.json preserves PASS and bound raw hashes;
  initial result.json FALSE preserved honestly (parser failure only).
- REA original module init reviewed, ev_6b8a4e5b4bcefd640fad18caf71d566beec48b186651b27bf64662c78062ad2e.
  Final module executable/version/static-key sections equal analyzed candidate
  byte-for-byte (rea-live-code-corroboration.json). Snapshot saved and CLOSED.
  Raw pmsg header is NOW OBSERVED, no longer unknown. Baremetal writer/cache/
  ownership/reset retention remains UNTESTED; do not equate Android with baremetal.
- USB baseline: current boot_b/vendor_boot_b SHA still matched exact backups.
  Normal adb reboot bootloader; fastboot getvar productk6895v1_64/current-slotb/
  unlockedyes/is-userspaceno/maxdownload0x4000000. Sent exact current Magisk
  boot_b backup64MiB SHAee817627... with fastboot boot (RAM download only).
  Sending65536KB OKAY1.381s; Booting FAILED(remote:'unknown command'), rc1.
  No flash/erase/set_active/OEM command. Issued fastboot reboot, rc0.
- Android RECOVERED: new boot ID, B/boot_completed1/root/Enforcing; boot_b
  ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10
  and vendor_boot_b bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670
  unchanged. Wireless autostart again tls-ready. Private evidence
  research/ace-fastboot-baseline-20261019/verification.json.
- Continued matching LK snapshot with REA: registration helper5b58 and
  download/flash registration8558 corroborated; bounded static search does
  NOT rule out alternate OEM paths.6754 is interior block, direct procedure
  query rejected; unknown-command string no xref in current Ghidra coverage.
  Runtime response decisive for STANDARD fastboot boot unsupported. New
  rea-lk-command-snapshot.json CLOSED, full limitation ledger retained.
- Profile adds raw-header result and observed fastboot unsupported, retains
  ios_deployable=false and adds verified-temporary-custom-code-entry-method
  blocker. docs/ACE-FASTBOOT-RESULT.zh-CN.md + status + diagnostic README.
- NEXT: resolve actual custom-code entry/continue/OEM registration paths in
  LK through bounded static work; do not issue debug OEM names blindly and do
  not assume temporary fastboot boot works. A concrete diagnostic image with
  observability/reset/rollback remains prerequisite. Any partition flashing
  needs per-step confirmation per user AGENTS; no unreviewed fallback writes.
  XNU/ADT/BootArgs/GIC/timer/MTK controllers/full iOS remain UNFINISHED.
- Milestone source/docs/profile/tests committed locally as e1a3741; no push.
  Final phone check: Android B/boot1/root/Enforcing/tls-ready, USB+TLS both
  authorized, no temporary probe module/file. All REA sessions CLOSED and
  agent work finished; no active device writer/QEMU at handoff.
- Host preflight PASS/no errors; full91 unit tests PASS in2.684s
  (4 new ANSI/invalid-observation regressions); exact
  QEMU and actual phone checks above. No new XNU build/CI run/push.

## Previous milestone (2026-10-19): wireless reboot recovery VERIFIED

- User saved Android current-network trust via always-allow checkbox. User
  explicitly requests future connections without repeated prompts. Do not ask
  for this authorization again on the same trusted Wi-Fi/paired host.
- Authorized TLS reconnected; initial startup attempt had timed out while
  waiting for user trust, preserved honestly in private before-test log.
- Issued another normal Android reboot with no requested phone interaction.
  Existing paired TLS transport returned through mDNS; boot ID changed;
  installed startup status matches CURRENT boot ID and says tls-ready,
  setting1/TLS port matches system current valid port. Boot completed1,
  PGKM10/MT6895/B/root0/SELinux Enforcing/ro.adb.secure1 and script hash all
  verified. PASS: research/ace-wireless-autostart-20261019/
  trusted-reboot-verification.json, hash-bound trusted-reboot-after.txt.
  Current Wi-Fi + existing paired computer scope only, no auth bypass.
- Host adb connect briefly added an IP alias alongside mDNS transport;
  compared boot IDs then removed only the matching duplicate alias. One
  authorized paired mDNS transport retained. No new pairing/key changes.
- Continued mainline with read-only /proc/iomem/ramoops parameter inventory.
  153 actual kernel ramoops resources continuous/no overlap, covering
  48090000..4816ffff, pmsg EXACTLY48160000..4816ffff. Earlier inferred pmsg
  range now independently corroborated by actual kernel resource registration.
  resource-layout-verification.json and bound snapshot under private
  research/ace-driver-port-20261019/pstore-retention/. Raw header UNKNOWN;
  /dev/mem,/dev/kmem,/proc/kcore absent. No node creation, mapping, module
  load, bare RAM write, image flash or partition write this milestone.
- Current iOS state remains UNFINISHED. Existing probe/bridge/protocol codecs
  are diagnostic/offline components. Next mainline: establish independently
  validated safe read/ownership/cache/reset path for baremetal logging, then
  observable actual entry/GIC/timer, XNU loader/ADT/BootArgs and MTK drivers.
  Do not claim diagnostic boot candidate is usable iOS; preserve Android and
  backups. Destructive writes still require per-step confirmation per AGENTS.
- Milestone documentation committed locally as f3185af; no push.
- Prior full tests87 PASS + bridge QEMU4 PASS; this milestone changes docs
  and records actual device checks only, no source changes/new CI/push.

## Previous milestone (2026-10-19): Ace entry/protocols; wireless trust pending

- User requests persistent wireless debugging and continuation of actual Ace iOS
  bring-up. iOS is NOT bootable on Ace yet. No partition/image writes this
  milestone; normal Android reboots only. Existing backups remain intact.
- Implemented ace/entry/ PC-relative EL1 entry / EL2-to-EL1 bridge, preserving
  x0 and refusing active MMU/cache; four actual QEMU cases PASS, including
  relocation and valid MMU-on refusal. research/ace-entry-20261019/
  verification.json binds sources and probe. This jumps to a diagnostic probe,
  NOT XNU; no Mach-O/ADT/BootArgs/GIC/SMP or hardware execution yet.
- tools/ace-probe-boot.py builds deterministic gzip and optionally an unsigned
  v4 diagnostic boot, preserving stock ramdisk/header fields except kernel size.
  Seven tests, independent AOSP unpack and extracted-payload QEMU EL1/EL2 pass.
  Candidate SHA0fe98860a5e3a63ce70cf797e65d3b9f0fbefff4664e0b479d5e28e45a1369fb,
  UNTESTED/unsigned/ios_deployable=false/hardware_test_recommended=false.
  Private research/ace-probe-wrapper-20261019/. Do not flash as iOS.
- ace/ufs_protocol.{c,h,md}: bounded read-only UPIU/UTRD/PRDT/SCSI codec,
  15 tests, ASAN/UBSAN 12000 inputs, freestanding ARM64 compile PASS.
  ace/tcm_protocol.py: TCM envelopes/continuation/LSB bitfields; 11 tests,
  10000 differential cases against official C helper PASS. Neither implements
  controller DMA/SPI submission, power/clock/IRQ or XNU disk/HID integration.
- Official sources pinned to kernel8baa5a377e2776402de745579cc3835d08ee1cca
  and vendor0c04020c19a68356afd49ce24f2ff95ee56c37e0. These are NOT proven
  exact running g6973d81cd2ac source. Actual original vendor_boot extraction
  parent-chain and REA UFS/touch/DRM snapshots saved privately under
  research/ace-driver-port-20261019/vendor-modules/. All REA sessions CLOSED.
- Read-only live UFS SCSI geometry + 64KiB GPT header/table: CRCs PASS,
  userdata LUN2/partition80, logical4096-byte LBA3514368..62476279,
  241507991552 bytes. No hardcoded target in codec. DRM debugfs temporarily
  mounted/read/unmounted: 1080x2412@120, primary XB24 linear pitch4352;
  current DMA/PA still UNKNOWN. S3910 SPI/TCM needs dynamic report descriptor.
- Actual ramoops backend settings read. Saved old pstore, wrote plain unique
  marker through normal Android /dev/pmsg0, normal reboot, retrieved marker
  in fresh pmsg-ramoops-0 (522B), changed boot ID/boot_completed1/B/root0.
  research/ace-driver-port-20261019/pstore-retention/status.json records PASS.
  This proves normal Android pmsg retention only, NOT bare RAM writes/reset.
  Inferred pmsg region48160000+10000/DBGC12B/ECC0 still needs raw-header proof.
- Installed tools/android-wireless-adb-autostart.sh as root0700 at
  /data/adb/service.d/90-ace-wireless-debugging.sh. Bounded Magisk late_start
  restores adb_wifi_enabled only, retains TLS/auth/SELinux; no legacy5555.
  Manual final run PASS: tls-ready/setting1/positive TLS port/secure1.
  research/ace-wireless-autostart-20261019/installation.json binds source hash.
- Issued normal reboot to validate autostart. User photo shows Android Wi-Fi
  debugging trust dialog AUTOMATICALLY appeared. Checkbox 'always allow on
  this network' is unchecked. Asked user to check it and allow: ADB/mDNS
  currently absent, cannot click remotely before authorization. Automatic
  TLS reconnection across reboot is NOT yet verified. Next: user allows,
  reconnect, inspect status and boot ID, then reboot again and verify automatic
  recovery with saved current-network trust. Do not alter trust XML/keys.
- Completed entry/protocol/wireless sources committed locally as 06c7104.
  No push. Wireless documentation now records photo-confirmed trust pending.
- Full final suite:87 unit tests PASS (1.889s); bridge QEMU4 separately PASS. New protocol docs: docs/ACE-PORT-STATUS.zh-CN.md and
  docs/ANDROID-WIRELESS-AUTOSTART.zh-CN.md. No new CI run, gh build or push.
- Added ace/pstore_ring.{c,h,md}, caller-owned pure-RAM DBGC/12B/ECC0
  ring codec:10 tests PASS including UBSan,1600 differential append rounds, ARM64 freestanding
  zero undefined symbols. Fixed pre-validation NULL pointer arithmetic in
  review. No physical addresses, initialization of unknown headers, cache
  maintenance, hardware writes or boot-entry integration. Full unit log:
  research/ace-driver-port-20261019/unit-tests-final.log.
- Codec/final test results and trust-pending docs committed as e06d52e,
  after main implementation06c7104. All agent work complete; no device
  writer or REA session remains active. No new CI run/push.
- Next device action remains user saving current-network trust, then verify
  reboot autostart. Next mainline action remains safe observable baremetal
  entry before XNU loader/controller implementation; iOS remains unfinished.

## REA + REAL CPU milestone (2026-10-19): all8 hardware16K capability verified

- Owner explicitly requested REA investigation, fixes, verification, then iOS
  flashing/running. iOS goal remains UNFINISHED: no MT6895 XNU/driver boot
  image yet. Do not flash userland alone or use SWEET boot image on Ace.
  No raw partition write/switch/reboot/SELinux/property change this milestone.
- Reused REA Ghidra12.1.4 raw ARM64 base0 LK snapshot, followed concrete
  boot_linux_fdt0xcf74, gzip0xbcfc, cleanup0x26ff0, physical trampoline0x26da8.
  Actual LK SMC at0xde70: x0=c2000115,x1=kernel,x2=DTB,x3=0,x4=1.
  Full primitive evidence saved research/ace-boot-entry-20261019/
  rea-lk-handoff-snapshot.json (27records); REA session CLOSED.
- Readonly acquired live lk_b/tee_b,5MiB each, before/after/local SHA matched.
  Private research/ace-secure-handoff-20261019/acquisition.json.
  LK_B SHA6c87c7158605359cc89404d9630632ca9455f31cc7b4b367ff9a6271c6b05ba8;
  TEE_B SHA11d84b56101eb117410d710bc533272b795c39edc1ff6b706994910c11c96d13.
  Both OTA prefixes byte-identical, zero-filled partition tails. ATF first
  MTK component289656B SHA082d229cc11e996b9b77dde9a88b52065ff9599be39626ae1d22b5badba71724.
  Local OTA tee/spmfw/gz/preloader extracted with manifest hashes, never flashed.
- ATF REA handler69c8 mapped by MTK_SIP_KERNEL_BOOT record3e000; generic SIP
  dispatcher removes FID. First64bit path64c4 selects SPSR3c9(EL2h) if PFR0
  EL2field present, else3c5(EL1h). One-time/condition flags preserved in report.
  Context setup7684/7528 and independent GNU restore at534c/59f4/5374 derive
  PC=kernel, x0=DTB on this static path. NOT physical custom-entry observation.
  Snapshot research/ace-secure-handoff-20261019/rea-atf-handoff-snapshot.json
  (9records), session CLOSED. Details docs/ACE-BOOT-ENTRY.zh-CN.md.
- Fixed probe to accept EL2 MMUoff, corresponding SCTLR/TCR/VBAR/SP and
  ESR/FAR/ELR bank, v2 record120B. EL3 still refused; never disable MMU or
  add MMIO/SMC/storage.8 actual QEMU cases PASS: EL1+EL2 success, relocation,
  BRK, valid MMUon refusal. EL2 PSTATE9/ownstack verified, MMUon preserves
  live SCTLR_EL2.M and page tables. Image12288B SHA
  4d53080a202b4874f94126eab319efe29cf0d88a5c14988c36795456fdfc11c0.
  New qemu-el2-mmu-on.S bound in verification and host preflight. Prior v1
  artifacts archived research/ace-offline/probe-v1-before-el2, not overwritten
  as claimed successful hardware evidence.
- Original kernel gzip from stock boot Image SHA
  8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0
  boots QEMU8.2.2 TCG virt/GICv3/virtualization on/CPUmax/1CPU/768MiB.
  First bounded45s test exited0 naturally24.351s: PID1, exactuname,3heartbeats,
  protected nVHE KVM init, powerdown. research/ace-stock-qemu-20261019.
- Supersedes earlier module dead-end: authentic live headers/config+normal
  Android12-5.10 Kbuild scripts/modpost+real OEM module symbol CRCs were enough
  for THIS minimal module. No need entire OEM kernel source. Prepared-tree
  comparison8832files unchanged; replay independently checks8830regular
  archive headers and430official script files.2895enabled config macros match. Partial symvers
  CRCs true(module_layout7c24b32d,printkc5850110); export metadata inferred
  from official contemporary source, runtime-validated for this candidate.
  Clang18 retains strictCFI/fullLTO/SCS/PAC/BTI/zero-init; compatibility patch
  removes obsolete zero-init acknowledgement flag only. Struct module1024/
  align64/init400/exit960 emitted by Kbuild, matches OEM. No fabricated struct,
  CRC, force-load flag or CFI bypass. Candidate/scmversion is own build.
- Module ace_read_regs.ko131864B SHA
  12655d3b3d8ecc3818d4541c800416975335cba37da2ef59f9cc228da3eac782.
  Only undefinedprintk. QEMU normal finit_module and delete_module PASS, same
  OEM kernel11.697s exit0: research/ace-module-qemu-20261019/run3/result.json.
  Preserve run1 harness compile failure and run2 loaded/unloaded but timed
  out because harness omitted poweroff; corrected run3 is full PASS.
- Committed replay source location diagnostics/ace-read-regs/: check-only and
  normal rebuild pass;8830archiveheaders/430scripts verified. Rebuilt candidate
 131896B SHA7e04f00c3dede4e00cd27aea1acf90e7c9edbbe225e564bbb265f33e58c05fc1
  separately passed QEMU run4-rebuilt14.150s/exit0/load+unload+powerdown.
  It was NOT phone-loaded; physical evidence binds original12655d... only.
- REAL PHONE: first normal insmod/rmmod both0; then8more runs pinned via
  taskset one CPU each, Cpus_allowed_list verified0..7. CPU0-3 MIDR412fd050
  (A55),CPU4-7 MIDR411fd411(A78); ALL MMFR0=101122/TGran16=1,
  CNTFRQ=13000000. Thus hardware16K CAPABILITY established on all8cores;
  16K page-table execution/XNU not tested. Each load/unload succeeded, no
  residual /proc/modules entry, phone tmp files+dirs removed. boot_completed1,
  tainted before/after4609 unchanged. Private research/ace-module-live-20261019/
  result.json and per-cpu/result.json preserve bound hashes and raw logs.
- Profile now records actual CPU corroboration, removes resolved transport/
  hardware16K blocker; restore path/final dynamic memory/custom boot/MTK
  drivers remain. Host preflight passes, ios_deployable=false.44 unit tests
  pass; no new XNU build/CI run/push. Preserve all backups and Android.
- Source/docs/profile milestone commit dd8c88e. All completed changes committed
  locally; no push. No running device command or pending writer at handoff.
- Next concrete work: build observable Ace baremetal boot/diagnostic wrapper
  matching proved gzip/vendorboot/ATF handoff; establish safe RAM/log retrieval
  before hardware execution. Then MT6895 XNU platform, interrupt/timer bringup,
  storage/display/input drivers and full iOS boot. Do not mistake working
  register module for XNU or attempt raw kernel-boot SMC from running Android
  (one-shot context protocol is not a safe general diagnostic API).

## LIVE wireless milestone (2026-10-19): connected, 19 backups VERIFIED

- Owner rebooted phone and enabled wireless debugging. Existing pairing
  auto-connected through mDNS. One authorized PGKM10/MT6895 device verified,
  Android boot_completed1, slot_b, bootloader unlocked. Plain ADB UID2000;
  su UID0 confirmed; SELinux Enforcing. No root-adbd/domain/property changes.
- Ignored/private research/ace-live-20261019-wireless/ final manifest all8
  reads OK. Initial inventory timeouts retained; optimized collector avoids
  process spawning per block attribute and filters platform basenames first.
  Live FDT488371B SHA256
  c20f9244e03b9353ef4304f2003387f1fdc0af6637251191899f19e9d0da9c4e.
  Profile matches,8GiB RAM [0x40000000,0x240000000),51 reserved-memory nodes
  (48fixed/3dynamic). Dynamic final allocations remain unknown; candidate
  unreserved windows are NOT certified safe baremetal load windows.
- Actual CPU4xA55(MIDR0x412fd050),4xA78(0x411fd411), all8online. DSI
  connected/enabled1080x2412; actual mipi-dsi driver
  oplus21861_boe_nt37701a_fhd_dsi_cmd, SPI2.0 synaptics-s3910.
  Framebuffer DT PA0xfe1af000/size0x1e50000; stride/format/runtime handoff
  unknown. IRQ snapshot timer27/UFS169/DSI355 active (touch EINT135 is not
  GIC INTID135). Reports hardware-analysis.json/.md in private capture dir.
- Boot-control32B CRC valid: A priority6/retries7/successful; B priority7/
  retries1/successful. Metadata does not prove past candidate execution.
- Valid backup research/ace-backup-20261019-wireless-v2: ALL19 VERIFIED,
  total578781184B. Both boot/vendor_boot/dtbo/vbmeta/system+vendor vbmeta,
  nvram/nvdata/nvcfg/persist/protect1/protect2/proinfo. Source before+after
  hashes and independent local reread hashes/length match. Added actual
  vbmeta_vendor_a/b whitelist. Initial directory without -v2 retained FAILED:
  adb exec-out merged remote dd stderr stats into raw stdout, caught by size
  bounds. Fixed remote dd 2>/dev/null; local real-dd regression added.
- boot_b current Magisk SHA256
  ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10;
  vendor_boot_b matches stock SHA256
  bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670.
  A/B boot and vendor_boot differ; preserve exact slot-specific backups.
- Readonly acquired kheaders.tar.xz3791452B SHA256
  e65e44a2ff42b6d3a1bbb9c34b768ee00be27fb88a65f31c5baed3b008b9bd05
  and OEM arm_dsu_pmu.ko38488B SHA256
  e4f929eaeaa6db5451d310fdee8e96d0791cb2331e9d971e4f5af7be54564a7b.
  Headers/vermagic match5.10.236-android12-9-o-g6973d81cd2ac. Two unsafe
  outward tar links skipped; no external link followed. OEM REA session
  closed with private oem-module-rea-snapshot.json saved.
- Module path: MODULES yes/modules_disabled0, SIG disabled; strict CFI,
  full Clang LTO and MODVERSIONS enabled. Headers lack root Makefile,
  scripts and Module.symvers; normal Kbuild exits2/no modules target.
  OEM built with Android Clang12.0.5 r416183b; local Clang18 TU experiment
  is not a loadable module or ABI proof. Private module-feasibility/report.md
  and verification.json preserve normal Kbuild exit2, TU strict-CFI/full-LTO
  plus SCS/x18/PAC/BTI compilation, .bc/.o only and input/output hashes.
  Official OnePlusOSS repo lookup
  for6973d81cd2ac returned422/no commit; v15 ace branch8baa5a377e2776402de745579cc3835d08ee1cca
  cannot be assumed matching. EL0 MRS emulation masks TGran16, so does not
  establish 16K support (Linux arm64 cpu-feature-registers documentation).
-44 unit tests pass. No CI dispatched or new XNU build/physical boot.
  No phone file push/module load/reboot/property/policy/slot/partition write.
  Next: recover exact kernel build inputs or another proven custom-code
  entry, then privileged CPU register read/16K capability and controlled
  boot diagnostics; MT6895 XNU/storage/display/input work still unfinished.
  ios_deployable remains false. Implementation/docs/test commit fdbb1d6.
  Final readonly check boot_completed1/slot_b/root0 succeeded; all19 verified
  entries independently re-counted578781184B. No ongoing device command.

## Ace host preparation (2026-10-19): offline milestones complete, live validation pending

- Implementation/docs/tests commit: cec628c. Previous userland image
  completion commit: f2ca099. No push or new CI dispatch.
- Owner requested exhausting work possible on the PC before reconnecting the
  phone. Implemented independent MT6895 profile/DT audit, readonly collector,
  bounded readonly backup tool, host preflight and CPU record probe. Details:
  docs/ACE-OFFLINE-AND-DEVICE.zh-CN.md. No physical Ace image or iOS boot claim.
- Installed Clang/LLVM/LLD18.1.3, QEMU8.2.2, GDB multiarch, Ninja, gh, gawk
  and dependencies. gh has NO account login. gh run view/auth checked; used
  connected GitHub fallback for existing public CI artifacts. No new CI run.
- Downloaded CI39158169212 (success, fdad0de8dc0e75c5ea84762adc03f7232dc91f19):
  xnu-kernel artifact12147422947 ZIP SHA256
  28a040196aa632af45b7ba6415831a09dd5098f7f9338b5ce6d1c146a9982b56;
  xnu-buildtree artifact12147962438 ZIP SHA256
  543d1a49ac334ebfc509573a0933fc93dd27744ae29464eca7c8c3f3a2985d21.
  Both verified; extracted research/ci-0081/buildtree, xnu/out-0081.
  Kernel SHA256d9cb893bd2baf841e94cd2001f0ec70c0fea42f045f87f14ae807e4ebc50e1e5,
  matches included SHA256SUMS. CI job117765628696 succeeded; decoded log tool
  returned transport closed, so full CI compiler log not acquired.
- Reference QEMU (4GiB/1CPU/mockfs tiny init, NOT Apple launchd or full iOS):
  original100s reached PID1+10 heartbeats, THEN IRQ latency panic15,777,808ns
  vs13,631,488ns threshold. Preserve original failure. Extra emulation-only
  interrupt-masked-debug-mode=1 (TRACE)100s reached PID1+13 heartbeats with
  no final-snapshot panic/unknown glyphs, exit0. Does not establish original
  config stability or identify the cause of latency. Report/logs/reproduction
  under research/ci-0081/qemu-baseline. GDB not enabled in those runs.
- Fixed qemu-sweet GDB to127.0.0.1 only; xnu-cc accepts XNU_CLANG/XNU_CLANGXX
  and bounded XNU_CC_JOBS (default<=4). Explicit local Clang C/C++ emission
  to ARM64 Mach-O tested, not a full local XNU compile. Original/current QEMU
  input-checksum lists retained with documented post-test GDB-only edit.
- Firmware DT SHA2562c262dd06c7fbc715ebd9462381addcb3ca92fb6b0bd6a6ec379893713fbfb91:
  GICD0x0c000000, GICR0x0c040000, timer13MHz/virtual INTID27, PSCI SMC,
  4xA55+4xA78 affinities0..0x700. DT audit handles4-cell GIC, dynamic carveouts,
  validates bounds/providers and distinguishes bus reg addresses from physical
  observations. These remain firmware configuration, NOT actual IRQ tests.
- Extracted embedded stock kernel config SHA256
  7d939635d77acbaa49a3e4ab2bdbb154c0a2c5e393b8057fa11a49071b56f149;
  KEXEC/KEXEC_FILE/DEVMEM disabled, MODULES enabled, MODULE_SIG disabled.
  This rules out direct standard kexec/devmem paths; module usability and
  exact vendor module ABI remain unknown. Android4K != CPU16K capability.
- CPU probe:12,288B Image SHA256
  13d6447529ebe7e6634745e70b5452b9d5da0ece10156ebd3e24744296e03f50.
  Built PIC/no ABS or unresolved symbols.5 QEMU cases pass: EL1 record,
  EL2 refusal, relocated execution, BRK exception, valid identity-mapped
  MMU-on refusal preserving SCTLR.M and page table. Does not touch unknown
  MMIO/UFS/GIC/display or execute SMC/reset. No Android boot wrapper. Live
  entry/hardware logging/record retrieval unknown. Verification now invalidates
  previous PASS before rerun and binds source hashes. EL0/EL3 not tested.
- Host preflight passed (research/ace-offline/readiness-complete.json); current
  ios_deployable=false and --require-ios-deployable returns2 intentionally.
  Boot/vendor_boot pins/v4/AVB bounds rechecked; root large-file checksums
  referenced from previously verified preparation, not redundantly rehashed.
-43 offline unit tests pass, including actual Clang Mach-O C/C++ output,
  image bounds, FDT4-cell/interrupt-parent/SPI bounds, output canonicalization,
  readonly collection/backup failures and stale probe evidence invalidation.
  Independent review issues fixed before final tests. Test log:
  research/ace-offline/unit-tests.log.
- Collector/backup have only mocked tests and dry-run/plan, NO phone calls.
  Output must be new ignored/private directory; transport serial not logged.
  Raw FDT/calibration remain private. Backup explicit whitelist/1GiB each,
  4GiB total, per-call bounds, before/after source hash and independently-read
  host hash+size; only then .img/verified. No restore/write functionality.
- Next after owner connects: stable authorized transport, readonly collection,
  live DT/iomem/panel/UFS/slot evidence, then verified actual device backups.
  Need proven custom-code entry before packaging probe, followed by real
  MT6895 XNU platform/storage/display/input work. No pending phone writer,
  reboot, daemon property change, or automatic device operation.

## iOS local preparation COMPLETE (2026-10-19)

- Owner goal: actual iOS on OnePlus Ace PGKM10/MT6895. Owner requested
  implementing documented firmware/root-image preparation. This milestone
  completes host userland preparation only. No Ace XNU/platform/driver build
  exists; SWEET kernel/image is not established as usable on Ace.
- Downloaded full iPhone X iOS16.7.16/20H392 IPSW from Apple's CDN, stored in
  ignored research/ipsw-x/. Source URL and IPSW.me index response retained.
  Size6,171,035,648B; SHA256
  ece1194f7e233e9109c5790a8d23a4564a10a254e15ec5b09978a343265568fb;
  SHA1 5606c298c1d908f8a48f617f0ceaf71f2a9f0193. Both match index. This is
  integrity comparison, not independent verification of Apple signatures.
- Apple BuildManifest confirms16.7.16/20H392, iPhone10,3/10,6. D22AP paths:
  OS087-86698-044.dmg(4,730,814,044B), SystemOS087-86593-047.dmg
  (2,743,074,816B), AppOS087-86715-047.dmg(10,485,760B).15 selected members
  extracted with ZIP CRC validation; extracted SHA256s independently checked
  before root build. Source mirror/DMGs retained, temporary chunks removed.
- D22AP device tree decoded/fully parsed:186084B, iPhone10,3,/product present;
  SHA2569e670987c80493bd69aba7be62e3179c04663324d9249b0973675baac175dbf1.
- Installed libfuse3-dev, libbz2-dev, zlib1g-dev, libattr1-dev, Android sparse
  image utilities and apt dependencies using owner-authorized sudo. Built
  APFS-FUSE66b86bd525e8cb90f9012543be89b1f092b75cf3 and LZFSE submodule
  e634ca58b4821d9f3d560cdc6df5dec02ffc93fd. Tool copies under ignored
  research/ios-toolchain/bin, linked from ~/.local/bin. AppOS FUSE mount/read
  actually tested and unmounted. No credential saved to files/scripts/docs.
- Ran project's mkiosroot.sh16G and sweet-root-tweaks.py on host image.
  Final raw: research/ipsw-x/ios16-root.img,17,179,869,184B (16GiB), SHA256
  7a5ce57e698b0724db024dece682c33f02e307d4ab6ad8da6336aa2af3052775.
  Final sparse: research/ipsw-x/ios16-root.simg,12,145,303,892B, SHA256
  b13d9d86c4aa1d22ba0e117e044130f579e717d88aeafa57296f75202c1811d4.
-49 content checks pass: launchd/dyld/SpringBoard present, root-owned0755;
  SystemVersion16.7.16/20H392; shared caches hard linked to cryptex copies.
  Post-tweak fsck.hfsplus -fn: volume iOSRoot appears OK. Sparse1.0/4096B
  blocks represents exactly16GiB; restored to temporary raw and cmp matched
  every byte. Temporary round-trip file deleted. Root builder exit0 and
  completion marker recorded. All temporary HFS+/APFS mounts released; all
  local preparation workers completed, no pending automatic operation.
- Evidence in ignored research/ipsw-x/: download.log, extraction-report.json,
  EXTRACTED-SHA256SUMS, adt-verification.json, root-build.log,
  root-content-verification.json, image-format-verification.json,
  ROOT-SHA256SUMS. Raw/sparse owned by xu; host disk about123GiB free.
- Recipe/result docs/IOS-LOCAL-PREP.zh-CN.md. Tooling/source milestone commit
  4e150e6. No CI run, XNU build, device write, reboot or boot test occurred.
  Earlier wireless transport/root-adbd blocker remains; next Ace work needs
  usable device transport, hardware evidence and MT6895-specific platform
  implementation. Userland image is ready; Ace iOS boot is NOT verified.

## Local environment audit (2026-10-19, read-only device inspection)

- Reviewed chat 01a15202-73f7-7582-bf2d-3dcd06b1ee8a. Owner goal is actual
  iOS on OnePlus Ace PGKM10/MT6895; root ADB is an intermediate bring-up task.
  Chat records wireless ADB pairing succeeded, but connection was refused;
  its last request was normal phone reboot and a new wireless connection port.
  This advances the older "await pairing details" handoff below. Pairing and
  current root were NOT reverified in this audit; `adb devices` is empty.
- Local project occupies about 7.7 GiB, mostly Ace Android artifacts. Present:
  PGKM10_15.0.0.1800_CN01.zip (7,234,973,868 bytes), extracted original boot,
  vendor_boot, lk, dtbo, vbmeta; Magisk v30.7 APK and patched boot; diagnostic
  vendor_boot versions v1-v5. These are Android/root/diagnostic artifacts.
- No iOS IPSW, Apple OS/SystemOS/AppOS DMG, iOS root image, compiled XNU
  kernel.development.*, or shim-boot image was found in the project, Downloads,
  searched home directories, or mounted media. Home scan excluded caches,
  .codex, node_modules and tool caches. The unrelated desktop Codex.dmg is
  an app installer. Author paths under /run/media/dipa are historical and are
  not locally available assets. No working MT6895 iOS boot image exists here.
- Available on PATH: adb/fastboot platform-tools37.0.1, AArch64 GNU GCC13.3
  and linker, mkbootimg, mkfs.hfsplus/fsck.hfsplus, CMake, Make, Python3.12.3.
  Missing on PATH: clang (also checked clang14/18), gh, qemu-system-aarch64,
  ipsw, apfs-fuse, img2simg, Ninja, Java. Root filesystem has about158 GiB free.
- No device write/reboot, download, kernel build, CI run or boot test in this
  audit. Next work remains restoring a usable device transport and obtaining
  MT6895 platform evidence; downloading iOS userland alone does not supply
  the missing loader/XNU platform/drivers.

## CURRENT root handoff (2026-10-19): su UID0 verified, USB hardware fault, await wireless ADB

**Proven milestone: `adb shell su -c id` returned uid=0/gid=0,
context u:r:magisk:s0.** Owner enabled Shell and Apps+ADB in Magisk; exact
result `root-adb/su-after-owner-grant.json`. Magisk boot_b installed, original
vendor_boot_b intact, Android B boot_completed1. No extra partition write.
Root can operate through su; plain root adbd is a separate unfinished test.

### True root adbd investigation (temporary runtime only)

- Pulled actual OEM APEX adbd, 2465712 bytes, SHA256
  53cd53860e9a8733b855cc519bc6a61d7dc1bc08e2fd8bbd8cab17093c6e600d.
  REA report/evidence `root-adb/oem-adbd-root-report.md`, native session closed.
  Production binary retains root branch. Initial `oem-adbd-init.rc` file is
  actually a cat path error; REAL init file is /apex/com.android.adbd/etc/init.rc.
- Real service argv `--root_seclabel=u:r:su:s0`, service userroot/seclabeladbd.
  Temporary resetprop ro.debuggable1, service.adb.root1 then ctl.restart adbd
  entered root branch but FATAL `Could not set SELinux context`; stock daemon
  recovered as UID2000 and service.adb.root0. Kernel audit specifically denied
  adbd->adbd process setcurrent. su type EXISTS (domain,coredomain); don't claim
  missing type. Root proc status/audit captured in root-adb/.
- Saved pre-test live sepolicy to ignored binary. Attempted live TWO rules:
  `allow adbd adbd process setcurrent`, `allow adbd su process dyntransition`,
  then reset root props/restart. Host command timed out without completion
  evidence; exact applied-rule/root-prop/process status must be rechecked.
  No persistent module/service.d or policy file installed, no global permissive.
  Reboot clears temporary policy/props. Do not repeat blindly or claim UID0 adbd.
- ro.adb.secure property stayed1, HOWEVER OEM logs explicitly say unlocked
  device disables auth / authentication not required. Property alone is NOT
  proof of effective USB auth. No intentional auth-disable change was made.
- For multi-command su: use one shell-quoted command (`su -c` + shlex.quote).
  Passing separate argv through adb shell loses quoting across semicolons.

### USB transport blocker and next step

- Actual current-functions/screen-unlocked-functions both MTP, debug settings1
  after owner selected File Transfer. Root diagnostics show repeated gadget
  disconnect/configure events. Host autosuspend control was ON (not auto).
- Host kernel subsequently reports **usb3-port1 over-current condition**, then
  repeated usb3-port1 AND usb4-port1 over-current (USB2/3 companion paths may
  share physical socket). These occurred after transport disappeared; no basis
  to blame SELinux rules for the electrical event. Phone remains normally
  operable per owner. Do NOT software-force-disable over-current protection.
- Owner reports changed port AND cable, but bounded20s poll still no phone USB
  enumeration; host continues over-current. No firmware flash can establish a
  repair of this physical link. Requested phone same Wi-Fi and Wireless
  debugging pairing IP:port/code plus distinct connection IP:port. Await these
  details to continue encrypted wireless ADB and verify root/USB configuration.
  Do not log/save pairing code or password; use interactive adb pair stdin.
- No rollback watcher or automatic phone flash is running. Original boot
  remains available if needed; root Magisk currently wanted by owner.

### Root installation/test history (below may describe earlier state)

**Now boot_b contains the authorized Magisk candidate.** Exact identity/product,
unlockedyes, currentb, boot_b64MiB and both hashes checked. Flash64MiB accepted:
send1.373s/write0.161s/total1.536s. Pre/post/preboot getvar b, both slots
successfulyes/unbootableno, retriesa7/b1. set_active b0.002s, normal reboot0.000s.
Root/Android boot verification pending; no claim of root yet. Log boot-flash.json.
Stock boot rollback helper prepared, NOT running. Do not duplicate flash.
Android B booted successfully at uptime23.96s. magiskd observed as root,
/debug_ramdisk/magisk reports30.7. Initially no su in PATH; full manager
environment repair completed with owner help and reboot; at uptime47.62s B
completed, /product/bin/su and magisk exist. Manager UI confirms installed30.7.
`su -c id` initially denied(code13); owner has since explicitly enabled Shell
and Apps+ADB in Magisk. Recheck has NOT yet reached phone because USB lost.
No claim of verified su UID0 or root adbd yet.
USB troubleshooting ongoing: host port power/control=on (not host autosuspend).
Repeated Android gadget re-enumeration observed ~30s apart; exact actor not
identified. After UI attempts/owner operation latest22d9:2046 descriptors show
Audio/MIDI ONLY, NO ADB interface. Cannot issue commands while in this mode.
Requested owner select File Transfer, enable USB debugging and set default USB
configuration. Do not treat this MIDI transport as an ADB permission problem,
or add unrelated udev rules. Avoid UI-coordinate actions while USB chooser can
interpose on another app. Fresh unique UI dump paths now used by ignored helper.
Next: prove `su -c id` UID0, inspect real APEX adbd, then temporary resetprop
ro.debuggable1 + service.adb.root1(-n) and ONE adbd restart; validate plain
adb shell UID0, auth remains1, actual daemon UID/caps/SELinux. Also acquire
USB service transition history and choose stable USB defaults; don't claim
popup fixed until connection survives observation window.

Owner requests root ADB and continued operation. Current stable Android B,
uid2000, ro.debuggable0/ro.secure1, no su; `adb root` explicitly rejected
production build. Original vendor_boot_b remains restored. Standard boot_b
Magisk path prepared instead of another unproven diagnostic recovery boot.
Official Magisk v30.7 APK SHA256 matches GitHub release digest:
e0d32d2123532860f97123d927b1bb86c4e08e6fd8a48bfc6b5bee0afae9ebd5.
Official source tag e8a58776f1d7bdf852072ad0baa6eceb9a1e4aac; APK boot_patch.sh
matches raw v30.7 script. Patched ON THIS DEVICE in a shell-owned temporary
directory with inspected official scripts/binaries, stock boot SHA pinned.
KEEPVERITY=true, KEEPFORCEENCRYPT=true, PATCHVBMETAFLAG=false, RECOVERYMODE=false,
LEGACYSAR=false; preinit metadata selected by tool. No partition written yet.
Candidate `research/ace-20261019/root-adb/magisk-boot-b.img`, 67108864 bytes,
SHA256 ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10.
Checks: original kernel/GKI signature bytes unchanged, boot header differs
only ramdisk_size; CPIO init is official magiskinit, original init backed up,
config flags checked; AVB footer bounds checked. Original signed hash remains
inconsistent with changed payload (normal Magisk repack; unlocked acceptance
still must be tested), no claim of OEM authentication or successful root.
Reports/logs under ignored root-adb/. Original boot rollback pinned SHA
6ab84213977b384d058d3c48545d23654313f5639b7a28fabfb3712dd9c57969.
Owner explicitly confirmed boot_b flash AND stock rollback in response.
No boot write yet; manager install failed/second attempt interrupted when USB
re-enumerated. Kernel journal shows regular ~30s USB reset; system uptime
continues, so not Android reboot. Completing normal first-run setup via
explicit-display0 UI before retrying manager installation and checking link.
Do not repeat consent for this same boot_b/rollback operation.
Update: normal setup completed, account login skipped, Android desktop reached.
Actual global developer/ADB settings were BOTH0 despite transient ADB access;
set both1, afterward official Magisk `adb install -r` returned Success. Owner
also reports installation complete. USB MTP+ADB and USB stay-awake enabled for
testing. Now proceeding with ALREADY CONFIRMED boot_b flash, select B and normal
boot. Mandatory stock boot rollback if no usable Android/root path.
Root su and true root adbd remain separate goals; after su first inspect actual
APEX adbd, then evaluate temporary debug property/adbd restart with ADB auth
kept enabled. No preloader/LK/GPT/vbmeta/verity/encryption modifications planned.

## CURRENT HANDOFF v5 (2026-10-19): stock restored, Android/control verified

**FINAL STATE: original vendor_boot_b restored; Android boot completed on B,
ADB authorized. No diagnostic remains intentionally installed.** Second reboot
after owner released all keys succeeded: completed1/_b/bootanim stopped,
PGKM10_15.0.0.1800(CN01), observed at uptime22.23s and152.89s. Initial Fastboot
return cause is not established. No pending rollback watcher/device write.
ADB uid2000, screenshot and input work. Touch with explicit display0 moved
GuidePage->LanguagePage; BACK returned GuidePage. No account/terms/setup
bypassed. UIAutomator dump failed null root; screenshot and activity state
supplied actual verification. Default tap did not establish navigation; use
`input touchscreen -d 0 tap ...` for this device.
No root ADB, live privileged hardware backup, XNU or iOS boot obtained.
Result: `diagnostic-v5-verified/test-result.json`; boot/control logs and images
beside it are ignored/private.

### v5 test observations and rollback history

Owner explicitly requested flashing, fixing errors and testing in the latest
message. Proceeding with the explained v5 diagnostic vendor_boot_b test, not an
iOS image. Starting ADB observed PGKM10, slot_b, boot_completed1, unlocked.
Both v5 and original recovery image SHA256 rechecked against pins below.
**v5 was flashed, then original vendor_boot_b restored (see result below).** Flash send65536KiB OKAY1.375s/writeOKAY0.141s/total1.518s.
Pre/post/preboot getvar current-slot all b; both slots successfulyes and
unbootableno, retry a7/b1 throughout; set_active b accepted0.002s. Reboot
recovery accepted0.001s. Diagnostic USB enumeration under observation.
Result: 40 enumeration polls detected NO ADB, Fastboot or matching phone USB
interface. Owner reports Recovery/language screen. Candidate execution/root
not established; footer repair did not establish a successful diagnostic boot.
Owner physically entered Fastboot; initially no USB enumeration, replug fixed
it. Rollback helper detected exact phone/product/unlocked and **restored stock
vendor_boot_b successfully**: send1.413s/write0.157s/total1.571s, set_active b
0.002s, reboot0.000s. Return Fastboot current-slot was **a**, despite preboot b.
Thus explicit set_active and corrected footer still did not establish candidate
execution; do not assert the failure cause. Initial reboot remained in Fastboot B (successful=no, retry6, unbootable=no);
owner then confirmed all keys released. Another normal reboot accepted0.001s.
Stock Android subsequently verified as above. Rollback watcher has finished;
no pending automatic phone writes.
Capture both slots before/after flash and after explicit set_active b, then
recovery-only boot. Restore original vendor_boot_b before normal Android boot.
If recovery exposes no USB, physical Fastboot entry is still required; no
software can operate the physical keys without a connected transport.
Log folder: `research/ace-20261019/diagnostic-v5-verified/`.
No boot/vbmeta/LK/preloader/GPT/calibration write is part of this test.

Further read-only LK routing analysis: current-slot is a priority comparison
(misc+0x800 slot priorities; equal chooses A), not a last-executed-slot log.
Recovery with nonempty A/B suffix uses normal mode0 load_vfy_boot and suffix
selection, not hardcoded A; standalone mode1 only if suffix empty. Therefore
post-test A does not establish that diagnostic B actually ran or kernel failed.
Evidence: `research/ace-20261019/lk-recovery-ab-routing-report.md` and matching
objdump. Next useful evidence is boot-control raw32 bytes across stages or
actual suffix/AVB/init boot log. Avoid another speculative flash without a
specific fix or improved observability. Physical Recovery/Fastboot transition
still requires owner help if USB interfaces disappear; ADB control cannot
press physical keys while no transport is exposed.

## Previous handoff: original vendor_boot restored, Android B booted (2026-10-19)

**Latest actual state: original vendor_boot_b restored; stock Android boots
successfully on slot B. No diagnostic image remains intentionally installed.**
Owner authorized the diagnostic write AND subsequent stock restore. No iOS
image has been flashed or booted. No live hardware dump or calibration backup
was obtained; the path to a usable Ace iOS system remains unproven.

### Completed device test and mandatory rollback

- Candidate v4 flash to vendor_boot_b succeeded (details/log below). First
  diagnostic boot showed stock-looking Recovery UI; no USB ADB in 35 s.
  Cannot claim root, permissive SELinux, or modified init ever ran.
- Owner's photos showed Recovery menu, then Orange State. No ADB/Fastboot USB
  transport was present then; software could not remotely change modes.
  Three-key suggestion did not establish Fastboot. Exact LK source inspection
  found GPIO127/Volume Down for project21861, security-state==3 gate to mode99;
  bootmode2 Recovery overrides key detection. Security-state meaning unproven.
  Asked complete power-off, Volume Down held while Power starts, then release
  Power/keep Down. Owner subsequently reported Fastboot; exact serial/product
  transport was detected. Do not promise all firmware accepts this sequence.
- At return to Fastboot: unlocked yes, product k6895v1_64, **current-slot a**.
  Thus stock Recovery display cannot establish whether candidate b executed.
  No raw-flash mark-unbootable/set_active call was found in bounded inspected
  handler/distributor code; indirect write callback remains partly unknown.
  Do not infer either automatic slot change or definite kernel failure.
  Offline LK analysis: `research/ace-20261019/lk-flash-slot-bounded-objdump.txt`.
- Already-authorized original rollback executed automatically on exact phone:
  flash original vendor_boot_b, 65536 KiB send OKAY **1.374 s**, write OKAY
  **0.137 s**, total **1.512 s**. set_active b OKAY **0.002 s**; reboot OKAY
  **0.000 s**, total **0.050 s**. Full log
  `research/ace-20261019/diagnostic-v4/stock-restore.json`.
- Android was then observed `sys.boot_completed=1`, `_b`, bootanim `stopped`
  at uptime **37.23 s**. Later checks remain booted/connected. Device state
  evidence `diagnostic-v4/restored-android-check.json`. Original host image hash
  verified before restoration; there is no privileged device-side hash readback.
- No other boot/vbmeta/LK/preloader/GPT or calibration partition written.
  All rollback watchers have completed, no pending automatic phone write loop.

### Next work (read-only before another device write)

- Latest continuation (2026-10-19): ADB confirms stock Android completed boot
  (`sys.boot_completed=1`, `_b`). **No phone write/reboot in this continuation.**
- Fixed the offline builder's missing AVB footer. New required `--avbtool`
  argument uses inspected AOSP source; rebuilds unsigned NONE hash metadata
  with the stock salt/property and fills the original 64 MiB partition size.
  Checks footer bounds, original payload size, `avbtool verify_image`, preserved
  vendor header/DT table/bootconfig and decompressed CPIO round-trip. Four host
  negative checks reject missing/bad/bounds-invalid footer and changed ramdisk.
- Latest **offline-only, NOT device-tested** candidate:
  `research/ace-20261019/diagnostic-v5-verified/vendor_boot-ace-diag-UNTESTED.img`,
  67108864 bytes, SHA256
  `c27fc48c27a4a12897e632180f4d20253a55d058d7385144a8a7f4d82422e7d0`.
  Payload 38952960 bytes, vbmeta offset38952960/size640. Reports and negative
  checks beside it. `diagnostic-v5/` is an incomplete earlier builder invocation
  (verification filename lookup failed); do not use that directory.
- AVB tools pin: `aosp-avb` c5066a96caa7bf4150c0a8cc8cc14ab81733fdc7;
  mkbootimg pin d2bb0af5ba6d3198a3e99529c97eda1be0b5a093.
- **Footer correction is NOT an established boot-failure fix.** Original
  top-level vbmeta has a direct vendor_boot hash (38776832 bytes), not a chain
  to vendor_boot's footer. It still mismatches changed contents. Inspected
  libavb source loads the full partition if ALLOW_VERIFICATION_ERROR is set;
  direct hash verification does not read that self-footer. Whether the shipped
  LK passes this flag or uses extra parsing is still unresolved. Unlocked
  status alone is not evidence of that call's flags. Do not write vbmeta as a
  speculative remedy. Existing v4 boot selection remains inconclusive.
- Further bounded shipping-LK disassembly confirms the relevant implementation:
  wrapper0x5e950 calls img_auth_required via0x37798->0x9133c at0x5e9cc;
  return0 sets flag bit0 at0x5e9e8, otherwise clears it at0x5ea10. Flags passed
  in w3 to avb_slot_verify0x72188 at0x5ec70/74. Hash loader0x735b4 tests bit0;
  enabled branch calls ops+88 to obtain full partition size before loading.
  Policy state3 boot/recovery table entries return auth-required0. Additional
  static trace ties state3 to Fastboot unlocked=yes: refresh0x79f0 calls
  0x377b0->0x9d6b0 (state!=3); zero result publishes yes at0x7a54..0x7a88.
  img_auth_required uses the same state getter. Actual boot-time arguments and
  recovery-specific branch remain unobserved (mode1 also ORs flag4). This
  narrows the earlier unknown; it does not prove why the previous test failed.
  Evidence: `research/ace-20261019/lk-avb-flags-shipping-objdump.txt` and
  `lk-avb-flags-shipping-policy.json` (synthetic base0 ARM64 offsets).
  Final detailed evidence: `lk-avb-flags-shipping-report.md`. No REA session
  opened in this bounded follow-up; no native session remains to close.
- Builder/footer milestone committed as `68bd770`. No CI build or device boot
  of v5 was run. Final ADB recheck still B/completed/orange/unlocked/bootanim
  stopped. Next unresolved tasks: establish actual boot policy and candidate
  selection, obtain controlled root diagnostics/live RAM map, then implement
  an MT6895-specific loader/XNU platform and drivers. Existing sweet image is
  for a different SoC; copying iOS root alone does not address these blockers.

- Resolve actual candidate selection/recovery loading and boot failure evidence.
  If a future approved test is made, capture pre/post flash and preboot current
  slot, unbootable/successful/retry-count for both slots; explicit set_active b
  removes some metadata ambiguity but does not prove candidate execution.
- Do not make speculative vbmeta/LK/preloader edits or claim the generic
  diagnostic candidate is a functioning Ace iOS port. No Ace XNU build exists.
- Keep original B boot path and restoration image ready. Distinguish the owner's
  target of usable iOS from proven capabilities; Android recovery was achieved,
  root diagnosis and iOS boot were not.

## Diagnostic v4 test history: stock rollback completed (2026-10-19)

**Do not boot normal Android until original vendor_boot_b is restored.**
Owner explicitly authorized the proposed diagnostic vendor_boot_b write and
subsequent stock restoration. Verified before write: intended phone, unlocked
**yes**, current-slot **b**, vendor_boot_b size 0x4000000; both input SHA256s
match the pins below. `fastboot flash vendor_boot_b diagnostic-v4/...img`
sent 38040 KiB OKAY 0.805 s, write OKAY 0.080 s, total 0.918 s, exit 0.
`fastboot reboot recovery` OKAY 0.001 s, exit 0. Diagnostic ADB test pending.
Device operation log: ignored `research/ace-20261019/diagnostic-v4/device-test.json`.

First result: no diagnostic ADB in 35-second poll. Owner reported language
selection; photo shows stock-looking Recovery with Format Data / Reboot / Power
Off, no bootloader menu. This does not prove the modified recovery init ran.
No hardware dumps/backups were acquired. **Original rollback is pending**;
Recovery has no USB interface and host cannot issue reboot from there.
Asked owner to enter Fastboot by previously successful method; if absent menu,
Power Off then try Power + Volume Up + Volume Down while USB connected.
Do not format or normal-boot while candidate is installed. Ignored helper
`research/ace-20261019/restore-stock-vendor-boot.py SERIAL` waits up to 45s for
exact device and then performs already-authorized stock vendor_boot_b restore,
selects B and reboots. Restore log is written only after device is detected.
Native Recovery picture has not established which slot actually booted;
query current-slot on next Fastboot before restoration (helper does this).


Mandatory rollback (already authorized by owner): reach bootloader, verify
slot b, then restore `research/ace-20261019/images/vendor_boot.img` to
`vendor_boot_b` (original SHA256 bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670).
Then ensure slot b and reboot Android; verify boot_completed=1 and ADB.
No boot/LK/preloader/vbmeta/GPT write was authorized or sent in this test.
If diagnostic ADB fails, do not repeatedly normal-boot; get Fastboot and restore.

## ACTIVE HANDOFF: stock Android restored, diagnostic test awaiting approval (2026-10-19)

**Latest observed state:** Android 15 is booted successfully on original slot B,
ADB authorized, Bootloader unlocked, no modified partition image flashed.
`sys.boot_completed=1`, `init.svc.bootanim=stopped`, slot `_b`, system_server
PID 1919 remained alive across >200 s of checks; focused activity is
`com.coloros.bootreg/.settings.activity.GuidePage` (initial setup).

### Recovery result and limits

- Owner brought phone to Fastboot. Queries: current-slot **a**, unlocked yes,
  slot-successful:a yes/b no, unbootable:a no/b no, retries a/b=7, two slots.
  This differs from pre-unlock Android's observed `_b`.
- Ran `fastboot set_active b`: OKAY 0.003 s. Immediate getvar still reported a;
  did NOT claim that was verification. Reboot OKAY 0.000 s. Actual Android
  after reboot confirmed `_b`, PGKM10_15.0.0.1800(CN01), flash.locked=0,
  verifiedbootstate=orange. Boot completion observed after ~2 min first boot.
- Inference: prior A-slot selection likely contributed to the restart issue;
  this is not proof of every cause. Do not assert a repaired A-slot or tested
  future reboot/slot-success state. Avoid further unnecessary restarts.
- Post-wipe data usage ~5.1 GiB vs pre-unlock ~110 GiB; no personal data read.
- Original full OTA now complete: **7234973868 bytes**, full streamed MD5
  **9ed76b5cd524c7fff4bf0b4d33cb75c5**, matches CDN header. Resume file gone;
  verification JSON `research/ace-20261019/full-ota-verification.json`.
  Whole archive is a verified download, not a tested emergency unbrick route.

### Concrete offline diagnostic artifact (not iOS)

- Added `tools/ace-recovery-diag.py`. It accepts only exact original H.20
  vendor_boot SHA, never invokes adb/fastboot or mounts/writes device partitions.
  Uses inspected AOSP mkbootimg checkout; no downloaded binaries in git.
- Final candidate **v4**:
  `research/ace-20261019/diagnostic-v4/vendor_boot-ace-diag-UNTESTED.img`,
  38952960 bytes, SHA256
  `05254fd6c24a79204c2180873d8543f656f88ab14260ee8ac613c58b6b5b8ff2`.
  Earlier v1/v2/v3 superseded, must not flash them.
- Changes: root/unauthenticated recovery ADB properties, permissive SELinux
  request, disable automatic Recovery/Phoenix/other unrelated services;
  strip all exec/exec_start, persistent-copy/property-load actions. All three
  ramdisk fstabs replaced with comments; /data,/cache,/metadata,/mnt/vendor/
  persist backed by tmpfs. Original kernel is in separate unchanged boot.img;
  vendor_boot DT table, addresses, fragment type/name/board IDs and bootconfig
  preserved. Base+overlay0 DTS has no fstab nodes.
- Verification: original pin checked, rebuilt 929-entry newc metadata/data
  round-trip, lz4 round-trip, repacked vendor_boot field/DTB/bootconfig byte
  comparisons, image size bound; malformed CPIO and wrong image format rejected.
  Independent read-only review of actual v4 found no further certain blocker.
  These checks do NOT prove boot success, root ADB, permissive SELinux, or
  absence of runtime persistent writes; those remain first-test questions.
- Narrow host udev rules also added for recovery USB 18d1:d001/4ee0.
- Prospective test requires **separate explicit owner consent to flash
  vendor_boot_b**, then recovery-only boot. Do NOT normal-boot with diagnostic
  image installed: its empty fstabs may prevent Android boot. Restore original
  `research/ace-20261019/images/vendor_boot.img` (SHA bb5a094d... above) to
  vendor_boot_b before normal boot, including failed-test recovery. Never
  relock or write LK/preloader/GPT for this test. A/B switching alone was not
  treated as authority for partition flashing. No diagnostic image sent yet.

## Incident history: Ace restart loop after unlock (2026-10-19)

**Priority is restore stable stock boot, not iOS or diagnostic flashing.**
Owner reports repeated restarts at OnePlus logo/Orange State after selecting
reboot from stock Recovery. Photo confirms text "Orange State / Your device
has been unlocked and can't be trusted / Your device will boot in 5 seconds".
This is an unlocked-bootloader warning, not by itself a diagnosis of the loop.
No cause of repeated restart has been established. Do not claim Android boot
completed after unlock; it has not been observed.

- Owner explicitly confirmed personal data backed up/unneeded and authorized
  standard Bootloader unlock plus wiping. Two 5-second confirmation windows
  timed out (commands returned OKAY but `getvar unlocked` stayed no).
  Third attempt with volume-up held: "Start unlock flow", OKAY 2.387 s;
  subsequent `getvar unlocked` returned **yes**. User may release volume key.
- Device battery was 96%, USB powered before unlock.
- Tested standard temporary boot using **unmodified, matched stock boot.img**:
  65536 KiB download OKAY 1.381 s; boot command FAILED `unknown command`.
  **No boot/vendor_boot/vbmeta/LK/preloader/GPT partition image was flashed.**
  The only destructive device action sent was the explicitly authorized unlock.
- `fastboot reboot recovery` succeeded; owner confirmed original Recovery's
  language/menu screen. Stock Recovery exposes no ADB transport in this mode.
  After owner tried rebooting into Android, they reported the loop above.
- Latest host checks: no phone in lsusb; empty adb and fastboot device lists.
  A bounded 20-second enumeration poll also saw no phone USB interface.
  Owner must use physical buttons to reach Recovery/Fastboot; host commands
  cannot reach the phone while neither transport is enumerated.
- Asked owner to force restart (Power + Volume Up ~10-15 s), release when
  display goes off, then try Power + Volume Down for stock Recovery. Awaiting
  actual resulting screen. Do not order reset/format until Recovery state is
  understood; no automatic relock or blanket firmware flash.

### Host/tooling and pending work

- Installed narrow udev rules `/etc/udev/rules.d/51-oneplus-ace.rules` for
  22d9:2765/2769 and 0e8d:201c, group plugdev + uaccess; rules reloaded.
  Admin credentials were provided by owner for installation, never saved in
  project files or reports. Do not add credentials to commands/scripts/git.
- Installed gcc-aarch64-linux-gnu (13.3.0), binutils, dtc, lz4, mkbootimg, aria2.
  Ubuntu mkbootimg script fails `import gki`; inspected AOSP checkout at
  `research/ace-20261019/aosp-mkbootimg`, commit
  d2bb0af5ba6d3198a3e99529c97eda1be0b5a093, works as fallback.
- Whole matching OTA download running with aria2 (8 connections), target
  `research/ace-20261019/PGKM10_15.0.0.1800_CN01.zip` plus `.aria2` state.
  Latest progress ~73%; apparent file length is sparse, NOT completion.
  After completion verify full MD5 against 9ed76b5cd524c7fff4bf0b4d33cb75c5.
  Five selected partition images were already SHA256-verified as below.
- Stock base DTB + DTBO entry0 combined successfully with fdtoverlay;
  pre-unlock Android properties reported dtb_idx=0, dtbo_idx=0. Saved combined
  DT only describes pre-bootloader defaults; actual patched RAM map unknown.
- Independent REA/objdump analysis confirms absence of standard boot command
  registration in bounded inspected LK code; report/evidence under ignored
  `research/ace-20261019/lk-fastboot-command-analysis.md` and sibling JSON/text.
- **Untracked experimental** `tools/ace-recovery-diag.py` was drafted before
  this incident. Not executed, not validated, not a ready device image; no
  diagnostic image flashed. There is a CPIO metadata round-trip assertion to
  repair before offline use. Suspend this work until stock boot is stable.

## Local Ace investigation / handoff (2026-10-19, Asia/Shanghai)

This local checkout now has a different target: the current owner's **OnePlus
Ace PGKM10 / OP5565, MediaTek MT6895**. The historical sweet phone, backups,
images and external-drive paths below belong to the upstream project; none
are evidence of artifacts or permission for this Ace. Objective: investigate
and implement an Ace XNU/iOS port if feasible, ultimately test on this phone.
**No Ace iOS boot or successful flashing has occurred.**

### Observed on the attached Ace

- ADB authorized; shell uid 2000. Official Platform Tools 37.0.1 installed at
  `/home/xu/.local/share/android-platform-tools/platform-tools/`, with adb and
  fastboot links in `/home/xu/.local/bin/`. No root executable found on PATH.
- Android 15, `PGKM10_15.0.0.1800(CN01)`, Linux
  `5.10.236-android12-9-o-g6973d81cd2ac`, active slot `_b`, Android page size 4096.
- `ro.boot.flash.locked=1`, `ro.boot.vbmeta.device_state=locked`;
  `sys.oem_unlock_allowed=1`. That last property does NOT establish successful
  unlock, a working vendor unlock route, or ability to boot unsigned code.
- Reading `/dev/block/by-name/boot_b`, live DT property contents, and
  `/proc/iomem` fails with Permission denied. No partition backup acquired.
- Platform sysfs names identify `112b0000.ufshci`, `11201000.usb0`,
  `14000000.dispsys_config`, `14017000.dsi`, `c000000.gic500`.
  These names are not a complete register map or driver specification.
- REA `inspect_adb_device` evidence:
  `ev_015832428ce0793063e968fbdd776b69c3c0ed5667682918c7a11ea38b048b57`.
- REA pulled `/vendor/etc/fstab.mt6895` (9126 bytes), SHA256
  `e01f5991ff895f34990fd8768605d71a0908f041278a3a64590e2a673643985c`;
  evidence `ev_303ecbeb5d38676ad5d11ca609c52ca725ea800867027f1959755e6fe27525c3`.
  It declares AVB/slot-selected logical partitions and encrypted F2FS userdata.
  Raw evidence stays in ignored `research/ace-20261019/`; do not commit dumps
  or serials. REA performed observations/file acquisition, not bootloader
  disassembly at that initial stage; subsequent firmware analysis is below.

### Source lead, inference, and next gates

- Official source: https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895
  Branch `oneplus/mt6895_v_15.0.0_ace`, pinned by git ls-remote to
  `8baa5a377e2776402de745579cc3835d08ee1cca`. Exact match to the running
  vendor build has NOT been established.
- Additional device observation: `ro.boot.prjname=21861`; do not assume
  project 22047 or Ace Racing/10R firmware is interchangeable.
- Pinned MT6895 SoC DT: `arch/arm64/boot/dts/mediatek/mt6895.dts` in
  the official commit above. Source leads: `drivers/scsi/ufs/ufs-mediatek.c`,
  `drivers/gpu/drm/mediatek/mediatek_v2/`, and `drivers/usb/mtu3/`.
  MTU3 requires a different USB implementation from sweet's DWC3 code.
  Board-specific DT selection and exact runtime correspondence remain unknown.
- Owner has no local firmware; matching OTA acquired as detailed below.
  A complete emergency restore procedure is still untested.
- Inference from live platform addresses and sweet source: this requires a
  new board port (boot shim/ADT, memory reservations, GIC/timer/PSCI, UFS,
  display and input); changing model strings cannot adapt the sweet image.
  Android's 4K page size does not prove whether hardware supports XNU's 16K.
- Next: confirm backup and destructive-unlock consent before any unlock;
  establish usable custom-image loading (temporary fastboot boot support is
  still unknown). Implement Ace diagnostic shim, then XNU early console, RAM
  root, storage/display/input and finally iOS userland. Preserve reserved RAM;
  CPU 16K granule and actual panel/framebuffer remain unverified.
- No Ace build, kernel CI run, unlock, erase, flash or iOS boot. One read-only
  Fastboot visit was performed (below). Existing sweet CI builds do not
  validate Ace. No proof yet that an Ace iOS port will succeed.
- The owner authorized research and modifications. Still confirm each specific
  destructive unlock/erase/write per AGENTS.md, with concrete consequences;
  do not treat upstream's 2026-10-15 consent as consent to erase this phone.

### Matching OTA and first bootloader reverse engineering (2026-10-19)

- Located candidate through ROMProvider's PGKM10 index; obtained metadata
  directly over HTTPS from the vendor OTA CDN. URL (research only):
  https://gauss-componentotacostmanual-cn.allawnfs.com/remove-8b6040d4526312ab77f6d0014c838229/component-ota/26/04/08/7dc957b3990f411fa0cf7da4c3a9406c.zip
- CDN HEAD: 7,234,973,868 bytes; MD5 header
  `9ed76b5cd524c7fff4bf0b4d33cb75c5`. Whole ZIP not downloaded or MD5-verified.
  ZIP metadata CRC verified, project 21861, version PGKM10_15.0.0.1800(CN01),
  post-build fingerprint and incremental exactly match observed device.
  That match is not an independent cryptographic vendor signature check.
- Selectively reconstructed five images using HTTP Range, protobuf manifest,
  REPLACE/BZ/XZ/ZERO operations; each operation blob and full resulting image
  SHA256 checked against payload manifest. Manifest minor version is 7;
  selected partitions need no old-image operations. Local extractor is in
  ignored research, not a general-purpose reviewed flashing tool.
- Verified SHA256 image hashes:
  - boot (67108864): 6ab84213977b384d058d3c48545d23654313f5639b7a28fabfb3712dd9c57969
  - vendor_boot (67108864): bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670
  - dtbo (3162112): 6ef303e3f15e44fbbad70940ac89ef1fb76145de84af9f2c4fc410edeaf3d219
  - vbmeta (8192): c468bb645cf986f5e3b6dc97554f45b5e64dcef1c5c0a1ae98788360c1045f47
  - lk (4153344): 53718ccc7fe3944a44979b49d92b7ef6f0af6e86c92c2e654601d848958c8ee0
- Original boot and vendor_boot headers are v4, unlike sweet build.sh's v2.
  vendor_boot contains a DT table; FDT starts at file 0x24ae040 (307960 bytes).
  Base DT confirms 4xA55 + 4xA78, PSCI, MPIDRs 0x000..0x700;
  dtbo has 20 indexed entries. Active overlay/panel and live RAM layout unknown.
  Official board source now found: `oplus6895_21861.dts` in pinned kernel.
  It has Synaptics S3910 over SPI and multiple panel candidates; source facts
  do not prove which physical panel this handset uses.
- LK first MTK component: original file offset 512, 1362784 bytes, SHA256
  `9e3f9fd53316fe7d64a5ed70eea5374489f9aed3e33b20511437f21e269e8511`.
  REA/Ghidra 12.1.4 imported ARM64 at **synthetic analysis base 0**, not a
  recovered physical load address. No firmware target code was executed.
- Decompiled 0x7a98: confirmation UI, physical-key wait, unlock-allowed gate,
  lock-state change and userdata-wipe calls, with failure paths. Gate 0x7fdc
  reads a flag associated with FRP. No attempt to patch/bypass these gates.
  Evidence `ev_40e88f877b37f52fa41a9e1c70f7ef65140a3ff7467b517569182aa8dfb3c840`
  and `ev_3e814cc841c3b1d9fd586a01a55e86ad0180089f1e274d4641eacb7d734a2bfd`.
  Function 0x5f488 contains vendor fastboot verification logic; its presence
  does not establish how unsigned temporary boots behave.
- Exported 13 REA records to ignored `research/ace-20261019/rea-evidence.json`;
  closed native session with `rea-lk-snapshot.json` (11 native records).
- Rebooted into Bootloader to query only. USB VID/PID 0e8d:201c initially lacked
  host permission. Initial query/reboot timed out without commands executing.
  User completed desktop polkit authentication; setfacl granted current user
  rw on that USB device node only (temporary; not persistent udev rules).
- Actual Fastboot query `flashing get_unlock_ability`: **unlock_ability is true**,
  OKAY 0.002 s, exit 0. `fastboot reboot`: OKAY, exit 0, total 0.055 s.
  No `flashing unlock`, erase, partition write, or GPT modification was sent.
  Backup/explicit consent still needed before invoking destructive unlock.

## Agent handoff / active work (2026-10-15, latest)

### >>> REA + Ghidra verified 2026-10-19 (supersedes missing-native-engine note below) <<<

- User requested a native engine for REA. Installed official **Ghidra 12.1.4** and full **Eclipse Temurin JDK 21.0.12.1+1**, user-local under `/home/xu/.local/share/rea/providers/`. Official download archive SHA-256 values verified (metadata retained in `downloads/`). REA remains 6.7.0, dedicated Node 24.22.0.
- Scoped official REA setup persisted `GHIDRA_INSTALL_DIR` and `JAVA_HOME` in `/home/xu/.codex/config.toml` REA environment. Explicit Node 24 launch restored after setup; CLI `/home/xu/.local/bin/rea` also exports these engine paths. Setup recovery backup: `/home/xu/.codex/config.toml.rea.backup.0cb7e29d38cd23dc3ab8da7067d093a8698cbde14e1eed943dc08025e6ef8e87.recovery`. All unrelated Codex settings unchanged (TOML comparison). Final scoped doctor **healthy=true**, Ghidra **available=true**, native decompiler/JDK checks pass.
- **Actual MCP native pipeline PASS**, using command/args/env from final Codex config: open own x86-64 ELF fixture with provider ghidra; search `rea_score` (initial import/analysis **32.16 s**); pseudocode and assembly; `main` callees resolve **0x401106**; close session. Ghidra correctly recovered signed negative check and `x * 7 + 0xd`. Recompiled recovered pseudocode: **2007/2007** selected inputs match original, including safe integer boundary cases. Input SHA-256 unchanged. Evidence, runnable MCP test, source, recovered code and report: `/home/xu/.local/share/rea/validation/native/RESULTS.txt` and sibling files.
- **Desktop restart verification PASS (2026-10-19):** after user reopened Codex, the live `mcp__rea` tools appeared in this chat. Direct calls to `open_binary(provider_id=ghidra)` and `procedure_pseudo_code(rea_score)` succeeded, reporting Ghidra 12.1.4 and the expected signed condition / `param_1 * 7 + 0xd`; `close_binary` succeeded. Desktop integration is now observed working. This run verifies a small x86-64 ELF only; ARM64/Mach-O/large iOS binaries not tested. No phone/build/boot/partition actions or CI runs. Handoff commit: find with `git log -1 --grep='Record verified REA Ghidra native decompilation'`.

### >>> REA installation 2026-10-19 (host tooling only; iOS state below unchanged) <<<

- User requested installation of https://github.com/morluto/rea for Codex and verification. Installed official npm `rea-agents@6.7.0` under `/home/xu/.local/share/rea/app`, with independent npm `node@24` runtime **v24.22.0** under `/home/xu/.local/share/rea/runtime` (system Node remains v18.19.1). CLI wrapper: `/home/xu/.local/bin/rea`.
- Official `rea setup --client codex --yes --json` completed `ready`, installed `/home/xu/.agents/skills/reverse-engineer-anything`, backed up `/home/xu/.codex/config.toml` to `.rea.backup`. Corrected the generated shebang-based command to explicit Node 24 + REA script arguments so desktop startup does not select system Node 18. Final `rea doctor --client codex --json`: **healthy=true**, Codex registration and skill **aligned**, 207 tools. `codex mcp get rea --json`: enabled. Parsed TOML comparison verifies all preexisting configuration values preserved.
- Actual protocol tests using the exact command/args from final Codex config: **initialize PASS** (rea 6.7.0), **tools/list PASS** (207), **JavaScript analysis PASS** (own fixture: describeFile export and node:path import recovered), **objdump file_headers PASS** (`/usr/bin/true`, x86-64 ELF). CLI JavaScript analysis also passed. Evidence and runnable test: `/home/xu/.local/share/rea/validation/`; concise report `RESULTS.txt`; setup/doctor JSON in parent directory.
- Limit: current desktop chat was not restarted, so reloaded desktop tool invocation is not yet observed. User must fully quit/reopen Codex to load registration. No Ghidra/Hopper/IDA detected or installed; deep native decompilation requires a supported engine. Tested JS/objdump features work. No phone/build/boot/partition actions and no CI runs for this host installation. Commit for this handoff: find via `git log -1 --grep='Record verified REA installation for Codex'`.

### >>> UPDATE 2026-10-18 (read first, then the 10-17 handoff below) <<<

**STATE at end of 2026-10-18 (evening):**
- On the phone: userdata = **image v15** (`/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v15.img/.simg`; = v14 + `/private/var/preferences/SystemConfiguration/preferences.plist` with one network service "USB Ethernet": Interface DeviceName ue0 Type Ethernet, IPv4 Manual 192.168.7.2/24 router 192.168.7.1, DNS 1.1.1.1 8.8.8.8, set "Automatic" as CurrentSet). Fallback image v14 (v12/v13 deleted).
- Kernels: **0078** = all 8 cores (`cpus=8`, cpu6/7 = A76, homogeneous SMP; mkadt now emits 8 CPU nodes; ADT `shim/out/sweet-0078hi.adt`); **0079** = display off/on via IOMFB selector 12 kern_RequestPowerChange(state) (fade over 6 vsyncs, then black; verified: power button gives "SWEET FB: display off/on"); **0080** = `SWEET NET: <proc> route add/delete/change ...` and `... add/delete address ...` trace (built, `shim/out/shim-boot-0080s.img`, NOT booted yet).
- **Internet over USB: not working yet.** Host side is ready (temporary iptables: FORWARD accept for 192.168.7.0/24 + MASQUERADE, comment "ios-sweet"; lost on host reboot). With v15 the phone sent no DNS and no outbound traffic (only mDNS/ARP) -> configd probably did not apply the service (or did, without default route/DNS). Next: boot 0080s on v15, watch `SWEET NET` lines (does configd add 192.168.7.2 / default route on ue0?). If configd ignores ue0 (not an IOKit IONetworkInterface; configd 1241.140.6 source in `research/configd-1241`, SCNetworkInterface createInterface needs IONetworkInterface -> controller (IOMACAddress, SelfNamed) -> bus), add IOKit stand-ins and/or rename the ifnet to en*.
- Live log listener (`nc -ukl 5140`) may still be running, writing `logs/live-0078s.txt`.

**LIVE LOG over USB (0077, boot 0077s): no more recovery round-trips.** Boot an image with `sweetusb=2`, run `tools/sweet-usbnet.sh logs/live-NAME.txt` on the PC: it waits for the phone's CDC-ECM interface, sets 192.168.7.1/24 (sudo) and prints/saves the kernel console the phone streams every 100 ms as UDP to 192.168.7.1:5140 (starts with the last 64 KiB). `ping 192.168.7.2` checks the link. Current image: `shim/out/shim-boot-0077s.img` (kernel 0077, ADT sweet-0069hi, cpus=6, sweetfb_noconsole=1, sweetfb_hz=30, sweetusb=2). The recovery pull (`tools/sweet-log-pull.sh`) is still the way after a panic/hang before USB comes up.

**🎉 USB networking works (boot 0076s, 18:24 local): `ping 192.168.7.2` from the PC answers in ~1 ms, 0 % loss (200-packet burst, 1500-byte frames, 512/1024-byte frames).** 0075: CDC-ECM function (bulk 0x81/0x01, interrupt 0x82 NETWORK_CONNECTION; host MAC 02:00:5e:77:ee:01) + kernel ethernet ifnet `ue0` (legacy output, header strip like if_fake) with 192.168.7.2/24 set from the kernel (proto_plumb + SIOCAIFADDR on an in-kernel socket). 0076: received frames into one cluster mbuf (mbuf_allocpacket gave a first mbuf of length 0 -> panic "Failed mbuf validity check: len -14"). Host side (Linux cdc_ether, interface `enp0s20f0u3u1`): `nmcli dev set IF managed no; sudo ip addr add 192.168.7.1/24 dev IF; sudo ip link set IF up`. Boot image `shim/out/shim-boot-0076s.img` (`sweetusb=2`). iOS itself does not see ue0 yet (configd needs an IONetworkInterface in IOKit).

**USB device mode works (boot 0074s, 17:45 local): the host enumerates the phone at high speed as `1209:0001 ios-sweet "Sweet iOS (USB bring-up)"`.** 0072 read-only probe: ABL leaves the USB30_PRIM GDSC and all 7 USB clocks on, DWC3 v3.20a (GSNPSID 0x5533320a) in device mode (GCTL 0x00112000), halted (DCTL RUN_STOP 0, DSTS 0x00d3de04), event buffer still at ABL's 0xfdfc8000, QUSB2 PHY alive. 0073 (`sweetusb=2`): DCTL soft reset, own event buffer (polled, interrupt masked), ep0 DEPSTARTCFG/SETEPCONFIG/SETTRANSFRESOURCE, setup TRB, RUN_STOP; control-transfer state machine as Linux ep0.c; descriptors: vendor class, no data endpoints. It ran but no event came: **0074** forces the VBUS session in the Qualcomm wrapper (QSCRATCH 0xa6f8800: HS_PHY_CTRL |= UTMI_OTG_VBUS_VALID(20)|SW_SESSVLD_SEL(28), SS_PHY_CTRL |= LANE0_PWR_PRESENT(24), as Linux dwc3_qcom_vbus_override_enable) -> connect + enumeration. Image `shim/out/shim-boot-0074s.img`. Black Phone app: main thread waits in -[VMVoicemailManager fetchAccounts] (sync XPC; voicemail needs the modem).

**Navigation works (boot 0071s on v14, log `logs/boot-0071s.txt`):** swipe up from the bottom edge returns to the home screen; app switcher works. Two fixes: **0070** pid_hibernate (syscall 435 was nosys on the macOS config -> SIGSYS killed SpringBoard in -[SBToAppsWorkspaceTransaction _didComplete] when an app left the foreground; the only CONFIG_EMBEDDED-only entry in syscalls.master); **0071** touches starting within 48 px of an edge carry kIOHIDDigitizerEventFromEdgeTip (UIKit `_UIEventHIDTouchEdgeTypeForHIDEvent` reads the digitizer EventMask 0xb0007 bits 0x800/0x1000/0x2000/0x40000). Diagnosed, not fixed: Settings (Preferences) SIGTRAP in PodcastsUI func_1cdc47c58: force-unwrap of `URL.volumeTotalCapacity` (nil on our HFS+ root). Phone/Photos/Messages show black (MobilePhone launches, no crash) - next: stack samples via boot-arg `sweetsample=MobilePhone,MobileSlideShow,MobileSMS,SpringBoard` (image `shim/out/shim-boot-0071s.img`).

**🎉🎉 MILESTONE 2026-10-18 ~15:30 local: iOS 16.7 SPRINGBOARD HOME SCREEN ON THE PHONE** (boot `shim/out/shim-boot-0069s.img` = kernel 0069 + ADT `shim/out/sweet-0069hi.adt`, image **v14**; log `logs/boot-0069s-v14-HOMESCREEN.txt`). Home screen with a few apps, Settings opens, Control Center / lock screen / notification center work, touch + buttons work, 6 A55 cores (`cpus=6`), `sweetfb_noconsole=1 sweetfb_hz=30`. Known issue: cannot leave Settings (home gesture / AssistiveTouch home do nothing) - to investigate.
What it took today (in order): 0058 HID services (Apple IOHIDFamily-1915 user client), 0059 iPhone X identity (hw.product etc.), 0060 SPMI keys + GENI touch, 0061 1125x2436 presented display, 0062 RPMh L11C touch power + IOPMPowerSource battery, 0063 GENI FIFO packing (Goodix GT9896), 0064 PRIV_WORK_INTERVAL grant (SpringBoard "Failed to create work interval"), 0065 SMP via PSCI (6 A55), 0066 crash map regions, 0067 console mute without cons_ops write, 0068 IOSurface lookup of an already-mapped surface returns base -1 (backboardd snapshot crash), 0069 UFS log flush 10 s. Image v13: CommCenter removed from launchd.plist, BKNoWatchdogs. **Image v14** = v13 + Setup skipped (`/var/mobile/Library/Preferences/com.apple.purplebuddy.plist` SetupDone/SetupFinishedAllSteps true, SetupVersion 11, daemonizeNeedsToRun false; purplebuddy.notbackedup mini-buddy flags false; managedconfiguration.notbackedup LockdownActivationIndicatesCloudConfigurationAvailable false; springboard MCForceShowCloudConfigurationUI false) + mobileactivationd data ark seeded (`/private/var/containers/Data/System/D90C94C4-F94E-4FCF-8A28-A93BE3846D8E/Library/internal/data_ark.plist`, -ActivationState Activated etc.) + MediaToolbox D22/D221/Default SubServerConfiguration StartRecorderServer=false (mediaserverd crash loop: portrait-filter prewarm called NULL GL). **Activation:** ADT /chosen certificate-production-status 0, effective-production-status-ap 0, certificate-security-mode 1, effective-security-mode-sep 1 -> mobileactivationd's native Hactivation branch (Codex `codex/activation/report.md`; alternative 4-byte daemon patch documented there). Fallback image v13; v12 deleted.

**🎉 TOUCH WORKS (boot 0063u on image v13, 2026-10-18 ~13:15 local):** tapping (i) on Setup's Hello opens the device-info sheet; swipe-up is recognised (spinner, then back to Hello - under investigation). Chain: RPMh L11C vote (0062, `bsd/dev/sweet_rpmh.c`) -> GT9896 @0x5d on GENI SE7 (0063 fixed FIFO packing: register address went out byte-swapped) -> sweet_hid_touch -> SweetHIDTouch -> backboardd. Battery icon OK (0062 SweetBattery IOPMPowerSource, static 100 %). **Image v13** (= v12 + CommCenter jobs removed from launchd.plist + `BKNoWatchdogs`=true and `FBLaunchWatchdogExceptions{com.apple.purplebuddy:100}` in /var/mobile/Library/Preferences/com.apple.springboard.plist): Setup no longer killed by the scene-create watchdog (it blocked in CoreTelephony getSubscriptionInfo -> CommCenter, Codex `codex/setup/report.md`; that report also lists how to skip Setup: SetupDone/SetupFinishedAllSteps/SetupVersion=11 in com.apple.purplebuddy.plist + activation check). v9 deleted, fallback = v12. Input latency ~1 min with 1 CPU -> Codex task 11 = SMP via PSCI (`codex/smp/`).

**INPUT WORKS (boot 0060u on a freshly flashed v12, log `logs/boot-0060u.txt`):** power, volume up, volume down reach iOS (PMIC -> sweet_keys.c -> SweetHIDButtons -> backboardd). Power locks/unlocks (screen "off" shows the kernel console because the panel never really turns off). **Device identity fixed: iPhone X** (home indicator, Face-ID-style Setup). Earlier test (0059u, `sweethidtest=15` fake Home presses) advanced Setup from Hello to the language list.
- **0058** HID: `iokit/Kernel/arm/hid/`: IOHIDEventServiceUserClient + IOHIDEventServiceQueue + IOHIDEvent compiled UNCHANGED from Apple IOHIDFamily-1915.140.3 (= exact version of the iOS 16.7 IOHIDLib, clone in `research/iohid-1915`) over our minimal IOHIDEventService (SweetHID.cpp: SweetHIDButtons consumer page 0x0C power 0x30 / vol 0xE9/0xEA / menu 0x40; SweetHIDTouch digitizer collections). C hooks `sweet_hid_key(key, down)` (0 power, 1 vol+, 2 vol-, 3 home) and `sweet_hid_touch(finger, down, x, y)`. HID logs go to IOLog. Boot-arg `sweethidtest=N` = fake Home press every N s.
- **0059** identity: hw.machine/hw.model/hw.target/hw.product from the ADT (macOS-config kernel used to answer "iPad8,6"/"Redmi Note 10 Pro"). mkadt: root compatible `D22AP|iPhone10,3|xiaomi,sweet|...`, model iPhone10,3, target-type D22, `/product` copied from the real D22AP device tree (`research/ipsw-x/d22ap.adt`, extracted from the IPSW, NOT in git), `/buttons home-button-type 2`. Codex report `codex/mg/report.md`: MG ProductType = sysctl **hw.product** (unrecognized -> iPod), HWModelStr = hw.target, HomeButtonType = `/buttons/home-button-type`; disk cache `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/com.apple.MobileGestalt.plist` (keyed by build + UUID only -> stale iPod answers survived; reflashed clean v12 to clear it).
- **0060** drivers by Codex (`codex/input/hw-report.md`): `bsd/dev/sweet_keys.c` (SPMI arbiter v5 observer reads, PON 0x810 bits KPDPWR/RESIN SID0, PM6150L GPIO2 SID4 0xc110; works), `bsd/dev/sweet_touch.c` (GENI SE7 I2C @0xa84000, starts 45 s after boot). Touch result: SE7 fw ok (proto 3) but **0x5d and 0x38 both time out -> touch IC unpowered** (L11C LDO needs an RPMh vote). Codex task 8 = RPMh client (`codex/rpmh/`), task 7 = battery (`codex/battery/`).
- **0061** (CI 39117078444): red status bar "rdar:45025538" = UIKit "No status bar visual provider for screen" (360x800 pt is no real iPhone). AppleCLCD now presents **1125x2436** (iPhone X) and shows the centered 1080x2400; touch mapped the same; ADT canvas 1125x2436. `sweetfb_native=1` reverts.
- Images: `shim/out/shim-boot-0060b.img` (0060 + /buttons ADT `sweet-0060hi.adt`). Next: 0061 image with ADT from current mkadt.

### >>> HANDOFF 2026-10-17 late (read this first) <<<

**STATE: iOS 16.7 Setup.app "Hello" screen is ON THE PHONE** (boot `shim/out/shim-boot-0057u.img` on image v12). Photo `/run/media/dipa/android/ios-sweet-work/MILESTONE-setup-hello-2026-10-17.jpg`. SpringBoard + backboardd + Setup run; nothing crashes in the GUI path. Remaining crash/relaunch loops: installcoordinationd (should be fixed by 0057, unverified), mediaserverd (VirtualAudio removed in v12, unverified), mobileactivationd (~100/boot, not analysed), bluetoothd + fairplayd.H2 relaunch constantly (no hardware).

**What is on the phone now:** userdata = image **v12** (`/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v12.img` + `.simg` + `.sha256`; v9 kept as fallback, v8/v10/v11 deleted or superseded). Kernel **0057** (`xnu/out-0057`, CI `39067532732`). ADT **`shim/out/sweet-0057hi.adt`** (QEMU twin `research/q0057-hi.adt`). Boot image **`shim/out/shim-boot-0057u.img`**. Boot args: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=ufsroot0 unentitled_ios_sim_launch=1 ignition_level=1 wdt_test=no_user_checkin ufsrw=1 rootrw=1 launchd_unsecure_cache=1 wdt=-1`.

**Build a phone image** (kernel K, ADT A): `python3 tools/mkpayload.py $K $A shim/out/payload-X.bin --cmdline "$B" && (cd shim && ./build.sh ../shim/out/payload-X.bin && cp out/shim-boot.img out/shim-boot-X.img)` then check `python3 tools/unpack_bootv2.py shim/out/shim-boot-X.img shim/out/check-X && cmp shim/out/check-X/ramdisk shim/out/payload-X.bin`. QEMU smoke test: `python3 tools/mkpayload.py $K research/q0057-hi.adt $S/csq/payloadX.bin --ramdisk $S/csq/root-fork.img --cmdline "debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=md0"` + `PATH=~/swift/usr/bin:$PATH python3 tools/qemu-sweet.py ... --secs 40 --kernel $K --fail-on-panic` (S = scratchpad; root-fork.img lives in the session scratchpad csq/ dir and may be gone in a new session).

**Kernel workflow:** edit `research/bt28/xnu/...` (keep the pre-edit copy in `research/preNNNN/`), syntax check `python3 tools/xnu-cc.py research/run28.log research/bt28 <file>`, make `xnu/patches/NNNN-*.patch` with `diff -u pre bt28 | sed` path rewrite, add new/changed files to `research/check-patch-order.py` list, run it (must say applied + MATCH), commit + push -> GitHub Actions `xnu` builds (~8 min) -> `gh run download <id> -R dipa-studio/ios-sweet -n xnu-kernel -D xnu/out-NNNN`. **Repo is PUBLIC since 2026-10-17** (private macOS runner minutes ran out: "recent account payments have failed"); public = free runners. Commit trailer: only `Co-Authored-By: dipa-studio <183933817+dipa-studio@users.noreply.github.com>`.

**Phone workflow (user does buttons, Claude runs commands):**
- Boot test kernel: phone in fastboot -> `fastboot boot shim/out/shim-boot-X.img`. NEVER `fastboot getvar`.
- **Read logs WITHOUT filming:** after a test the user holds Power+VolDown -> fastboot -> `fastboot boot recovery/recovery.img` (OrangeFox, temp) -> wait for `adb shell true` -> `tools/sweet-log-pull.sh /run/media/dipa/android/ios-sweet-work/logs/<name>.txt` (reads the 4 MiB console ring the kernel keeps in the last 1025 blocks of userdata; patch 0047). Then `adb reboot bootloader` brings the phone back to fastboot without the user.
- **Flash a root image:** `fastboot flash -S 512M userdata <img>.simg` (7 min, 25 chunks). After a big flash the Xiaomi ABL fastboot hangs: next `fastboot boot` stalls at "Sending" -> the USER must re-enter fastboot by hand (Power+VolDown). Do not retry commands against the hung ABL. A flash right after `adb reboot bootloader` once failed on chunk 1 (USB protocol error): just retry. User must NOT unplug during flash (once interrupted at 25/25 -> reflash).
- **Edit the phone root without reflashing (same-length only):** find the file's raw offset in the local image (it is one extent; search the image for its first 4 KiB), compare with `adb exec-out dd if=/dev/block/sda34 ...`, then `adb push` changed 4 KiB blocks and `dd of=/dev/block/sda34 seek=... conv=notrunc,fsync`, read back. Recovery kernel has no hfsplus.
- **Pull the whole phone root** (12 min): `adb exec-out "dd if=/dev/block/sda34 bs=1048576 count=16384" > img`; mount ro with udisksctl or `sudo mount -t hfsplus -o loop,ro`. To write into a pulled image: `sudo fsck.hfsplus -fy` first (volume is never cleanly unmounted -> Linux mounts ro even with -o force), then `sudo mount -t hfsplus -o loop,force`.
- Making images: copy latest img with `cp --sparse=always`, mount rw with force, change, `sync; umount`, `sha256sum`, `img2simg`. Keep only the latest image + one fallback on the SSD (/home is ~98% full; big work files live in `/run/media/dipa/android/ios-sweet-work/`, old kernels/images archived in `.../ios-sweet-work/archive/`).

**Diagnostics built into the kernel (all SWEET-only):** persistent console log (0047, boot-arg sweetlog=0 off; flush every ~1 s); `|name| text` copies of /dev/null writes for processes in `sweetnull` (default backboardd,SpringBoard; 0048); `IOK name:` IOKit lookup/open trace for `sweetiolog` (default backboardd,SpringBoard; 0049/0054, 400 lines max); `SWEET Sandbox: proc op N` (0050); `STR ...` heap text dump on SIGABRT/SIGTRAP for `sweetscan` (default backboardd,SpringBoard; 0051/0053) - this is how NSException/BSAssert reasons were found; `SMP name tN pc .. bt ..` user stack sampler for `sweetsample` (default SpringBoard,backboardd; first at 90 s then every 120 s, 40 samples, 16 frames; 0054/0055); `SWEET FB: N swaps` every 1000 swaps; `CRASH name ...` crash reports (0043/0044). Symbolicate cache addresses with `ipsw dyld a2s research/dsc/dyld_shared_cache_arm64 <addr - slide>`; main-binary addresses: addr - mh + 0x100000000.

**Patches added today (0046-0057, all CI-built):** 0046 IOSurface (IOCoreSurfaceRoot) + IOMobileFramebuffer (AppleCLCD on /arm-io/disp0) + arm-io nubs; 0047 persistent log; 0048 /dev/null tee; 0049 IOKit trace; 0050 permissive "Sandbox" MAC policy; 0051/0053 heap text on crash; 0052 RENAME_SWAP via exchangedata on HFS; 0054/0055 sampler, swap counter, AKS selectors 35 (extended device state = 17) and 101; 0056 panel copy from the vsync timer at 10 Hz (sweetfb_hz) instead of every swap; 0057 no config_ext_resolver (ACL group entries resolve without memberd). ADT (tools/mkadt.py): /arm-io/disp0, /chosen/display-scale 3, /chosen/unique-chip-id (synthetic 0x5357454554000001) + chip-id 0x8015 -> IOPlatformUUID A9683613-3704-53F2-95D0-98A8FB574E78. Image v9-v12: /private/var/containers/{Bundle,Data/System,Shared/SystemGroup,Temp}; launchd.plist StandardOut/ErrorPath renamed to ...PatX (pointing jobs at /dev/console stops them launching: EACCES); v12: LastSystemVersion=20H392 in plain /var/mobile/Library/Preferences/com.apple.migration.plist (stops the 1-hour data migration that ran every boot), VirtualAudio.plugin moved to /Library/Audio/Plug-Ins/HAL.disabled/.

**Codex helper** (`codex exec --skip-git-repo-check -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write -C /run/media/dipa/android/ios-sweet-work/codex -o OUT "$(cat task.md)" < /dev/null`, run detached with setsid nohup; config already defaults to gpt-6.1-sol high). Reports in `/run/media/dipa/android/ios-sweet-work/codex/`: mediaserverd-report.md, installcoordinationd-report.md (-> 0057), ufs-performance.md (ranked UFS speed plan), **ufs/0058-sweet-ufs-faster.patch** (READY, not yet applied: ufslogsecs default 10 s log flush batching, optional ufscache=1 directional cache ops, optional ufswait=1 spin-then-sleep; syntax-checked, host-stub verified; see ufs/README.md). Apply it as patch 0058 after review.

**Claude safety-classifier note:** several messages about QuartzCore renderer selection / writing an HFS reader tool were cut off by an automatic classifier (false positives, user agrees). Keep those topics short or let them be; they are not blockers now (rendering already works).

**NEXT STEPS (in order):**
1. **Input** (Setup stuck on Hello): touch + power + volume as IOHIDEventService/IOHIDDevice services backboardd matches (log shows backboardd matching IOHIDDevice with DeviceUsagePairs and IOService with HIDServiceSupport=true). Phone hardware: Goodix/Focaltech touch over I2C/SPI (check live DT `dtb/`), buttons via PMIC (pon) and GPIO keys. Start with a fake HID service (e.g. power button via a timer or boot-arg) to learn the ABI, then real drivers.
2. **Device identity**: MobileGestalt reports iPod + Home button. Add /product node / product-type (iPhone10,3, D22AP), device class iPhone, home-button-less (Face ID) properties in mkadt; find exact MG keys (MGIOMFBSupport.c, `IODeviceTree:/product` lookups seen in backboardd trace).
3. **Battery**: AppleSmartBattery/IOPMPowerSource style service (status bar shows empty red battery).
4. Apply Codex 0058 (UFS speed), consider cpus>1, check whether installcoordinationd/mediaserverd loops are gone, analyse mobileactivationd.
5. Hide kernel console over the GUI when not debugging: boot-arg sweetfb_noconsole=1 (but then panics are not on screen).

- **🎉 MILESTONE: iOS GUI ON THE PHONE - Setup.app "Hello" screen (2026-10-17 ~21:30 UTC, boot 0057u on image v12).** Photo: `/run/media/dipa/android/ios-sweet-work/MILESTONE-setup-hello-2026-10-17.jpg` (animated "dobar d(an)" hello lettering, status bar "iPod" + battery icon, bottom "Pritisnite Home za otvaranje" = "Press Home to open" (locale hr), (i) button). Rendered by iOS 16.7 SpringBoard/Setup through CoreAnimation -> backboardd -> kernel IOSurface (IOCoreSurfaceRoot) -> kernel AppleCLCD swaps -> ABL panel memory. What made it: data migration finally skipped (v12: `LastSystemVersion` 20H392 in the plain `/var/mobile/Library/Preferences/com.apple.migration.plist`; ADT `/chosen/unique-chip-id` + `chip-id` for IOPlatformUUID), 0057 (no ext resolver -> ACL containers work), plus everything before (0046 display/IOSurface, 0050 Sandbox policy, display-scale 3, containers dirs, RENAME_SWAP, AKS 35/101, 10 Hz present).
  **Missing (next work, in rough order):**
  - **Input: no touch, no power button, no volume buttons** (no HID drivers; backboardd looks for IOHIDDevice / HIDServiceSupport services). Setup is stuck on "Hello".
  - **Device identity: it thinks it is an iPod with a Home button** (status bar "iPod", "Press Home to open"): MobileGestalt has no product/model identity (no /product node, product-type, etc.) - give it iPhone10,3 / home-button-less (Face ID class) identity.
  - **No battery detection** (no battery/charger/PMIC service; status bar battery shows empty/red).
  - Locale came up Croatian (hr) - harmless.
  - Performance: cpus=1, polled UFS (Codex UFS patch in progress: `codex/ufs/`), backboardd presents at 60 Hz.
- **README refreshed (2026-10-17):** read the full notes and updated the public overview through patch 0045, v7 hardware observations and prepared v8 diagnostics. Documents real Apple userspace, the missing display/IOSurface GUI work, limited security services, highmem, persistent userdata root, current tooling and build examples. Documentation only; no kernel build, tests, flashing or phone boot performed.

- **v11 still migrated (boot 0056u, 20:32 UTC, `logs/boot-0056u-v11.txt`).** On iOS kCFPreferencesCurrentHost lands in the plain plist: all DMEnvironment setters (setLastBuildVersionPref, setUserDataDispositionPref, ...) use CurrentHost and the phone's `/var/mobile/Library/Preferences/com.apple.migration.plist` holds DMUserDataDisposition; datamigrator's XPC service runs with `_RoleAccount: mobile`. **Image v12** = v11 + `LastSystemVersion` = 20H392 added to that plain `com.apple.migration.plist` (keeps DMUserDataDisposition, 501:501 0600) + `/Library/Audio/Plug-Ins/HAL/VirtualAudio.plugin` moved to `/Library/Audio/Plug-Ins/HAL.disabled/` (Codex: stops the mediaserverd SIGSEGV loop; untested). **installcoordinationd loop explained (Codex `codex/installcoordinationd-report.md`):** os_crash "Failed to create data directory" EACCES for `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.installcoordinationd/Library/InstallCoordination`: `Library`/`Library/Caches` in the container are ACL-only (uid/gid 0xfffffffe, mode 0000, ACE for group GUID ...012B = gid 299 systemusers); with `config_ext_resolver` the kernel asks an identity resolver (memberd/opendirectoryd) that iOS does not run -> EWOULDBLOCK -> ACE skipped -> EACCES. **Patch 0057**: drop config_ext_resolver from FILESYS_BASE (compatibility UID/GID<->GUID mapping is used instead), likely fixes other ACL-protected containers too. Codex task 3: UFS driver performance design (`codex/ufs-performance.md`).
- **mediaserverd SIGSEGV loop explained (Codex report `/run/media/dipa/android/ios-sweet-work/codex/mediaserverd-report.md`):** the fault (FAR 0x390) is in the HAL plug-in `/Library/Audio/Plug-Ins/HAL/VirtualAudio.plugin/VirtualAudio` (ApplyBeamFormerPreference <- VirtualAudio_PlugIn::SetPropertyData <- HALS_AHPPlugIn::ObjectSetPropertyData <- AudioObjectSetPropertyData <- MediaExperience vaemVADSerializationListener): the default virtual audio device ('vdef', VirtualAudioDevice_Default) does not exist (no audio hardware/driver, no /product/audio). Proposed workaround for GUI bring-up: move VirtualAudio.plugin out of /Library/Audio/Plug-Ins/HAL/ in the next root image (untested). v11 reflashed OK after an interrupted flash (USB unplugged at chunk 25/25). Codex task 2: installcoordinationd crash loop.
- **ROOT CAUSE of the endless migration: no IOPlatformUUID (2026-10-17).** datamigrator's `-[DMMigrator isMigrationNeededWithBuildVersion:lastBuildVersion:clientPID:]` gets lastBuildVersion from `-[DMEnvironment lastBuildVersionPref]` = `CFPreferencesCopyValue("LastSystemVersion", "com.apple.migration", kCFPreferencesCurrentUser, kCFPreferencesCurrentHost)` -> a ByHost file. The phone had `/var/mobile/Library/Preferences/com.apple.migration.plist` (only DMUserDataDisposition) and NO `Preferences/ByHost` directory at all. On arm XNU publishes IOPlatformUUID (gethostuuid) only from `/chosen/unique-chip-id` (8 bytes) + `/chosen/chip-id` (4 bytes) (IOPlatformExpertDevice::generatePlatformUUID, called from IOPlatformExpert::start); the SWEET ADT had neither, so every CurrentHost preference write failed. Fix: mkadt adds `unique-chip-id` = 0x5357454554000001 (synthetic) and `chip-id` = 0x8015 -> UUID `A9683613-3704-53F2-95D0-98A8FB574E78` (same SHA1 namespace computation as the kernel). ADT `shim/out/sweet-0057hi.adt`, boot image `shim/out/shim-boot-0056u.img` (0056 kernel + 0057hi ADT, QEMU OK). **Image v11** = v10 + `Preferences/ByHost/com.apple.migration.<UUID upper and lower>.plist` {LastSystemVersion: 20H392} (501:501, dir 0755 files 0600). Flashing v11 2026-10-17 ~20:10 UTC. Codex (gpt-6.1-sol high) analysing the mediaserverd SIGSEGV loop in `/run/media/dipa/android/ios-sweet-work/codex/` (report `mediaserverd-report.md`).
- **v10 did NOT stop the migration (boot 0056n on v10, 19:18 UTC, `logs/boot-0056n-v10.txt`):** datamigrator + migrationpluginwrapper ran again, backboardd drew the progress UI (13000+ swaps in ~5 min). So `com.apple.DataMigration.plist`/LastSystemVersion is not the deciding input. What is known about the decision (datamigrator XPC service `DataMigration.framework/XPCServices/com.apple.datamigrator.xpc/com.apple.datamigrator`, strings): `Migration sentinel present. Migration necessary.` (sentinel `/private/var/datamigrator/migrate`, created and removed by datamigrator itself; absent in v10), `System build version changed from %@ to %@. Migration necessary.` / `...unchanged... not necessary`, `Disposition dictionary with build version %@ is out of date relative to current build version %@`, `SyntheticDidUpgrade`, DMUserDataDispositionManager; previous build source not found yet (not in the binary's plain strings; likely in DataMigration.framework's DMUserDataDispositionManager / preferences domain `com.apple.migration`). backboardd calls `DMPerformMigrationIfNeeded` and holds SpringBoard in `checkInAndWaitForDataMigration` until it returns. NEXT: find where the previous build version / disposition dictionary is stored (disassemble DataMigration.framework DMUserDataDispositionManager + datamigrator's isMigrationNeeded path), write it into the image; or get datamigrator's os_log out (OS_ACTIVITY_DT_MODE needs a launchd env change).
- **Data migration never records completion -> skip it (image v10, 2026-10-17).** Boot 0056n (18:16 UTC, `logs/boot-0056n.txt`, 30 min): 10 Hz panel copies, backboardd still presents at ~60 Hz (107k swaps), SpringBoard still in `BKSSystemShellService _checkIn` at sample 14. Every migration run takes 1+ hour on cpus=1 and repeats each boot. DataMigration decides from `/var/mobile/Library/Preferences/com.apple.DataMigration.plist` key `LastSystemVersion` (vs ProductBuildVersion 20H392); the pulled phone root (21:01 local) had NO such file. **v10** = that pulled phone state + fsck.hfsplus -fy (volume was marked not cleanly unmounted -> Linux mounts it read-only even with -o force; fsck found only hard-link counts + minor volume header, repaired) + `com.apple.DataMigration.plist` {LastSystemVersion: 20H392} (501:501 0600). `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v10.img` (+ .sha256, .simg); v8 files deleted, v9 kept as fallback.
- **Repo made PUBLIC (2026-10-17, user request) so GitHub-hosted macOS runners are free:** the 0056 CI run was refused ("recent account payments have failed or your spending limit needs to be increased"). Checked before: no device dumps, serials, IMEI or Apple binaries in the history (.gitignore keeps backup/, dtb/, recovery/, research/ out); commit author emails are public now. 0056 rerun `39056660104` passed -> `xnu/out-0056`, QEMU OK, image `shim/out/shim-boot-0056n.img` booted 18:16 UTC.
- **Boot 0055n (17:16 UTC, ~65 min, `logs/boot-0055n.txt`): migration bar reached 99% in ~30 min (was ~60), then crawled.** Root cause of the slowness: backboardd presents the progress UI at ~58 Hz (**167,000 swaps in ~48 min**) and AppleCLCD copied the full 10 MB frame into the panel on every swap -> ~600 MB/s memcpy on the single CPU (cpus=1), starving everything (polled UFS I/O too). Sampler (16 frames): **SpringBoard waits in `-[BKSSystemShellService _checkIn]`** (synchronous BSXPC call to backboardd, from FBSystemShellInitialize <- SBSystemAppMain) - backboardd holds the system shell check-in until the data migration ends, so the migration is the gate to SpringBoard UI. **Patch 0056**: swap only records the latest swap record; the vsync timer copies it to the panel every 60/sweetfb_hz ticks (default 10 Hz); `SWEET FB: N swaps` every 1000.
- **Boot 0054n (16:53 UTC, ~12 min, `logs/boot-0054n.txt`, patch 0054 sampler):** the data migration runs AGAIN on every boot (it completed once in the 0053s run) - completion is not being recorded. backboardd keeps swapping the progress UI (3700+ swaps in ~10 min, `SWEET FB: N swaps`). Sample during migration: SpringBoard main thread blocked in a synchronous XPC call (`mach_msg2_trap <- dispatch_mach_send_and_wait_for_reply <- xpc_connection_send_message_with_reply_sync <- -[BSXPCServiceConnectionMessage _sendSynchronously:] <- BSXPCServiceConnectionProxy ...`). Unsupported AKS selectors seen: 101 `aks_assert_consume`, 93 `aks_get_internal_info`, 34 `_aks_stash_load` (datamigrator), **35 `aks_get_extended_device_state`** (SpringBoard, chronod, remindd, searchd, symptomsd...). **Patch 0055**: AKS 35 answered like 17 (same DER device state), 101 succeeds; sampler backtraces 16 frames, 40 samples (~80 min).
- **MILESTONE: FIRST iOS PIXELS ON THE PANEL (boot 0053s long run, 15:33 UTC, ~60 min; photos IMG_20261017_183029/183222/183419; log `/run/media/dipa/android/ios-sweet-work/logs/boot-0053s-long.txt`, 407 KB, 1428 flushes).** The iOS data-migration boot screen (Apple logo + progress bar) was shown and the bar advanced to full in ~60 minutes. It is drawn by **backboardd through our kernel display path**: `SWEET SURF: backboardd create id 2/3 1080x2400 fmt 0x42475241 (BGRA) bpe 4 bpr 4352 size 10452992 keys 11`, IOSurface sels 9, 27, 5, 34 and traps 2/3 (lock/unlock), IOMFB SwapBegin (4) / SwapEnd (5, 1132-byte struct) / GetLayerDefaultSurface (3) / 68 / 55, then `SWEET FB: swap N layer 0 surface 2|3 1080x2400 ... a 0,0 1080x2400 b 0,0 1080x2400` alternating (double buffering; only the first 16 swaps are logged). Triggered by `com.apple.datamigrator` (AKS sels 101/93/34 return unsupported) and `com.apple.migrationpluginwrapper`. Probably ProgressUI-style CoreGraphics drawing into IOSurfaces (no GPU used). After the migration: SpringBoard and backboardd stay up (exec once each, no crash), nothing new drawn; crash loops only for mediaserverd, installcoordinationd, mobileactivationd (~108 each in the hour); bluetoothd and fairplayd.H2 relaunch constantly (no hardware). Kernel console text overlays the image (sweetfb_noconsole=1 would hide it).
- **MILESTONE: SpringBoard and backboardd both stay up (boot 0053s on v9, 15:29 UTC, `logs/boot-0053s.txt`).** With /chosen/display-scale = 3: `exec SpringBoard` once, `exec backboardd` once, no CRASH for either; MobileGestaltHelper reads IOMFB size/dot pitch; backboardd opens AppleCLCD (sels 57,15,22,29,33,79,74 as before). No IOSurface creates and no swaps: backboardd keeps polling `IOProviderClass IOAcceleratorES` (-> 0 found) and AGXAccelerator/IOAcceleratorESLegacy - no GPU, so no CoreAnimation renderer yet. Log goes quiet after ~47 s (only 47 flushes): the system idles. NEXT WALL: CoreAnimation rendering without a GPU (CPU path) so the window server produces frames.
- **SpringBoard's invalid mode = scale 0 (boot 0053n, 15:19 UTC, `logs/boot-0053n.txt`, heap scan):** `FBSDisplayMode cannot be configured as requested : <FBSDisplayMode: ...; infxinf@0x (1080x2400/0) 60Hz sRGB SDR>` - pixel size and 60 Hz are fine, scale is 0. libMobileGestalt (MGIOMFBSupport.c, sub_19c560a54) reads `display-scale` (u32, default 0) and `display-rotation` from **IODeviceTree:/chosen**, pixel size via IOMobileFramebufferGetDisplaySize (MobileGestaltHelper sel 8/28 in the log). mkadt now adds `/chosen/display-scale` = 3 (1080x2400 @3x = 360x800 pt). ADT `shim/out/sweet-0054hi.adt` (QEMU `research/q0054-hi.adt`), image `shim/out/shim-boot-0053s.img` = 0053 kernel + 0054hi ADT. Possible catch: MobileGestalt may have cached scale 0 in `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/...`.
- **MILESTONE: backboardd survives and opens the display (boot 0052n on v9, 15:07 UTC, `logs/boot-0052n.txt`).** No `CRASH backboardd`. It walks `IODeviceTree:/arm-io` children, matches IOMobileFramebuffer, `open AppleCLCD type 0 -> 0x0`, calls IOMFB selectors 57, 15, 22, 29, 33, 79 (GetBlock, out 1580/40), 74 (SupportedFrameInfo), 12, 6, 27, 17, 84, 50; opens IOCoreSurfaceRoot (sel 13); looks for AGXAccelerator / IOAcceleratorES / IOAcceleratorESLegacy (none, repeatedly), `IODeviceTree:/product` (none, repeatedly), `/buttons`, aop-smart-cover, IOPMrootDomain. No swaps yet. **SpringBoard now gets past display discovery** and dies (sig 5) in `-[FBSDisplayMode _initWithWidth:height:preferredScale:scaleOverride:refreshRate:gamut:hdr:rotation:virtual:validityCheck:]+580` <- `_initWithCADisplayMode:scale:rotation:` <- `FBSDisplayConfiguration _initWithImmutableDisplay:` <- `FBSDisplaySource initWithDisplay:` <- `FBSDisplayMonitor` (slide 0x14504000): "FBSDisplayMode cannot be configured as requested". Checks: width/height >= 2, preferredScale > 0, scaleOverride >= 0, refreshRate non-zero, valid gamut/HDR/rotation. Suspects: refresh rate 0 (IOMFB timing blocks answered with zeros) and/or scale 0 (MobileGestalt main-screen-scale; no /product node in the ADT). **Patch 0053**: heap text scan also on SIGTRAP and for SpringBoard (default sweetscan list backboardd,SpringBoard) to read the exact mode description.
- **Image v9 (2026-10-17) = v8 + `/private/var/containers/{Bundle,Data/System,Shared/SystemGroup,Temp}` (root:wheel 0755; on iOS these live on the data volume, absent from the rootfs) + launchd.plist with StandardOutPath/StandardErrorPath renamed to ...PatX (the in-place phone fix; daemons' stdout reaches the log via the 0048 /dev/null tee).** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v9.img` SHA256 aa9f9139...6e67, `.simg` 12,145,303,864 bytes; written through `sudo mount -t hfsplus -o loop,force`. **Patch 0052** (`xnu/patches/0052-sweet-hfs-rename-swap.patch`, CI `39042761826` -> `xnu/out-0052`, QEMU OK, image `shim/out/shim-boot-0052n.img`): vn_rename falls back to VNOP_EXCHANGE when VNOP_RENAMEX(RENAME_SWAP) returns ENOTSUP for two regular files on one volume (HFS exchange swaps data and cnode descriptors = swap semantics). Flashing v9 started 2026-10-17 ~15:00 UTC.
- **backboardd EXCEPTION FOUND (boot 0051n, 14:41 UTC, `logs/boot-0051n.txt`, patch 0051 heap scan):** `*** Terminating app due to uncaught exception 'NSInvalidArgumentException', reason: '*** -[NSURL initFileURLWithPath:]: nil string parameter'`. First-throw stack (slide 0x337f0000): `+[NSURL fileURLWithPath:]` <- `-[BSSystemContainerForCurrentProcessPathProvider libraryPath]` <- `cachesPath` <- backboardd main+0x1d858 (StartWindowServer, shader cache path). BaseBoard: libraryPath = `BSSystemSharedResourcesDirectoryForIdentifier` = `BSSystemSharedDirectoryForIdentifier(id)` + "/Library"; that calls `container_system_path_for_identifier` (libsystem_containermanager -> `_container_legacy_lookup` -> containermanagerd XPC), which returned NULL (BaseBoard logs "Error getting shared system container ..."). With 0050 the sandbox denials are gone. containermanagerd.log.0 in the pulled (pre-0050) image: "Did not receive any persona attributes", "Expected to find at least one persona", notify_register_dispatch failed 9; `/private/var/containers` does NOT exist in the root image (on iOS it lives on the data volume). usermanagerd does create kernel personas 99/199/1000, but fails to save `/private/var/keybags/usersession.kb` and `persona.kb`: "Failed to atomically swap writing file: Operation not supported (45)" (HFS has no RENAME_SWAP). NEXT: create `/private/var/containers` (and check what containermanagerd needs for system group containers), fix or emulate RENAME_SWAP on HFS, then re-check backboardd.
- **Disk housekeeping (2026-10-17):** /home was at 4 GiB free. Moved (not deleted) `xnu/out-0010..0044` and old `shim/out/*.img`/`payload-*.bin` (everything before 0046) to `/run/media/dipa/android/ios-sweet-work/archive/{xnu,shim-out}` (6.3 GiB); /home now 8.7 GiB free. Large work files (phone-root.img 16 GiB, logs, tracev3 dumps) live in `/run/media/dipa/android/ios-sweet-work/`. **Patch 0051** (`xnu/patches/0051-sweet-crash-heap-strings.patch`, CI `39041440935`): on SIGABRT of a process in boot-arg `sweetscan` (default backboardd) the crash log prints heap text runs as `STR ...` (to find the NSException reason). Boot 0051n 14:41 UTC.
- **Boot 0049n (14:11 UTC, `logs/boot-0049n.txt`, patch 0049 trace): backboardd's IOKit lookups before it dies** (each run): `IODeviceTree:/arm-io/pearl-sep` -> none, matching ApplePearlSEPDriver -> none, `IOService:/IOResources/AppleKeyStore` open OK, matching IOHIDDevice (DeviceUsagePairs) / `HIDServiceSupport` notifications, `usb-drd,t8027` notification; **never any IOMobileFramebuffer / display lookup** - the exception happens before display detection. launchd (tracev3) shows backboardd's mach lookups denied with `error = 159: Sandbox restriction`: com.apple.mobilegestalt.xpc, com.apple.iohideventsystem, com.apple.system.notification_center, com.apple.logd, containermanagerd, ACCHWComponentAuthService, oscard. libsystem_sandbox uses `__mac_syscall("Sandbox", op, arg)` (ops: 1 init, 2 check, 3 note, 4 container path, 5/6/7/8 extensions, 0x15 check_bulk, ...); with no policy named "Sandbox" every call gets ENOPOLICY. **Patch 0050** (`xnu/patches/0050-sweet-sandbox-policy.patch`): built-in permissive MAC policy "Sandbox" in sweet_amfi.c (mpo_policy_syscall returns 0, container/extension ops ENOENT; logs first use of each op as `SWEET Sandbox: proc op N`).
- **Phone root pulled (16 GiB, 12 min, `adb exec-out dd if=/dev/block/sda34`) to `/run/media/dipa/android/ios-sweet-work/phone-root.img` (loop-mounted ro at /run/media/dipa/iOSRoot).** No .ips crash reports. logd tracev3 (Persist, LZ4 `bv41` blocks, decompressed strings in `ios-sweet-work/tracev3/all.txt`): /private/var/db/uuidtext is EMPTY so only launchd's own messages are readable. Findings: v8 launch failure = `Service could not initialize: posix_spawn(/usr/libexec/backboardd), error 0xd - Permission denied` (xpcproxy exit 78) - /dev/console not openable for the mobile user; backboardd[98] spawned `com.apple.MTLCompilerService` before SIGABRT; **launchd denies many mach lookups with `error = 159: Sandbox restriction`** (mediaserverd -> com.apple.backboard.display.services, remoted, mobiletimerd -> sleepd, identityservicesd -> apsd) and **tccd exits OS_REASON_SANDBOX "profile not found"** - no Sandbox kext/profiles on SWEET; likely cause of many daemon crash loops (next wall after the display). CF's uncaught-exception text never reaches stderr for daemons (no CF handler; libc++abi prints only the type). **Patch 0049** (`xnu/patches/0049-sweet-iokit-trace.patch`): `IOK name: ...` console lines for registry path lookups, child iterators, matching (with result count/class), matching notifications and IOServiceOpen of the processes in boot-arg `sweetiolog` (default backboardd), max 400 lines.
- **CONFIRMED: launchd StandardOut/ErrorPath=/dev/console stops backboardd from launching.** After the in-place rename (boot 0047n-b, log `logs/boot-0047n-b.txt`) backboardd launches again and dies as on v7: sig 6, `___pthread_kill <- abort <- demangling_terminate_handler <- _objc_terminate <- std::terminate <- _dispatch_client_callout <- _dispatch_once_callout <- main+0x9334` (window-server dispatch_once). It never opened AppleCLCD or IOCoreSurfaceRoot (no `SWEET FB/SURF: backboardd` lines) -> throws before/at display detection. **Patch 0048** (`xnu/patches/0048-sweet-devnull-tee.patch`, CI `39037749668` -> `xnu/out-0048`, image `shim/out/shim-boot-0048n.img`): writes to /dev/null by processes named in boot-arg `sweetnull` (default `backboardd,SpringBoard`) are printed as `|name| text`. Boot 0048n (13:48 UTC, log `logs/boot-0048n.txt`): only `|backboardd| libc++abi: terminating due to uncaught exception of type NSException` (CF's reason line goes to os_log, not stderr, despite CFLOG_FORCE_STDERR/OS_ACTIVITY_DT_MODE). Next: pull the whole 16 GiB root from recovery (`adb exec-out dd if=/dev/block/sda34`) to `/run/media/dipa/android/ios-sweet-work/phone-root.img` and read ReportCrash .ips files / logd tracev3 for the exception reason.
- **Persistent log WORKS (boot 0047n on v8, 13:31 UTC; pulled from OrangeFox: 70 KB, 111 flushes, `/run/media/dipa/android/ios-sweet-work/logs/boot-0047n.txt`).** In 3 min **backboardd was never exec'd** (v7 ran it), ~70 bare `exec xpcproxy`, SpringBoard loops on FBSDisplayMonitor (no display), mediaserverd sig 11 loop, locationd, lockdownd sig 5. Suspect the v8 plist (StandardOut/ErrorPath=/dev/console on backboardd). **In-place plist edit from recovery (no reflash):** launchd.plist is one extent at image/partition byte offset 0x1e025f000 (195 blocks; verified bytes identical on phone vs local v8 mount); renamed StandardOutPath->StandardOutPatX and StandardErrorPath->StandardErrorPatX (same length, both jobs) in blocks 68 and 105 via `adb push` + `dd of=/dev/block/sda34 seek=... conv=notrunc,fsync`, read back VERIFIED. Phone now differs from local v8 image in those 2 blocks (files in `/run/media/dipa/android/ios-sweet-work/`). Test boot 0047n 13:38:42 UTC. Recovery kernel has no hfsplus (raw block edits only).
- **Patch 0047: persistent console log (CI `39036478663` -> `xnu/out-0047`, QEMU no panic; phone image `shim/out/shim-boot-0047n.img` = 0047 + sweet-0046hi.adt + 0045n cmdline).** `_cnputs` (all console output: kernel printf + daemons' /dev/console) also appends to a 4 MiB ring in sweet_ufs.c; after the UFS partition is ready and writable (ufsrw=1) a thread writes new ring blocks + header to the LAST 1025 blocks (4 KiB) of userdata every ~1 s and SYNCHRONIZE CACHE (prints `SWEET LOG: console log to the last 4100 KiB ...`). Read: phone to fastboot -> `fastboot boot recovery/recovery.img` (OrangeFox) -> `tools/sweet-log-pull.sh OUT.txt` (adb dd of that area + `tools/sweet-log.py`). Not yet verified on the phone. Panics after the last flush are not in it (screen still shows them). 2x font attempt reverted: XNU's v_scale only scales the progress icon.
- **Boot 0046n on v8 (13:05 UTC, VID_20261017_150522_HSR_120):** phone prints `SWEET SURF: IOCoreSurfaceRoot registered` and `SWEET FB: AppleCLCD 1080x2400 stride 4320 at 0x9c000000, default surface 1` (nubs + match work on hardware). Visible userspace: early boot tasks, launchd_cache_loader, `exec SpringBoard`; no `exec backboardd` / `SWEET FB: backboardd` line seen in the readable frames (video blurry). Frame 00:47: lower half of the screen shows OLDER console text (16:01:12) below newer lines -> unconfirmed hint that a swap copied an old snapshot of the panel (CA reads the default/displayed surface = panel memory). SpringBoard still dies in `-[FBSDisplayMonitor _initWithBookendObserver:transformer:]+1160` (sig 5, slide 0x30960000). **Shim: 2x console font** (`shim/loader.c` Video.v_depth scale field = 1) so phone videos are readable; image `shim/out/shim-boot-0046b.img` = 0046n + 2x font.
- **Patch 0046: built-in IOSurface + IOMobileFramebuffer (2026-10-17, offline, NOT phone-tested).** `xnu/patches/0046-sweet-iosurface-iomfb.patch`: new `iokit/Kernel/arm/SweetSurface.{h,cpp}` (IOCoreSurfaceRoot + IOSurfaceRootUserClient: sel 13/0/4/34/35, traps 0-5, wired buffers mapped into the caller, per-client refs) and `SweetFramebuffer.cpp` (AppleCLCD : IOMobileFramebuffer on /arm-io/disp0: sizes, swap = CPU copy of enabled layers into the ABL panel memory, 60 Hz vsync via sendAsyncResult64WithOptions(CanDrop), panel memory published as the default IOSurface, kernel text console paused on the first swap only with `sweetfb_noconsole=1` (default keeps the console: pausing switches it to serial and would hide panics)); SweetPlatformExpert creates nubs for /arm-io children (not gic) attached to the platform expert (IOPlatformDevice::compareName casts its provider to IOPlatformExpert, so nubs under the arm-io nub never matched - first CI build showed that in QEMU). mkadt: /arm-io/disp0 {device_type display-subsystem, compatible sweet,display, canvas-width 1080, canvas-height 2400}. CI `39021572169` -> `xnu/out-0046`. **QEMU** (`research/q0046-hi.adt`, RAM disk init, msgbuf): `SWEET SURF: IOCoreSurfaceRoot registered`, `SWEET FB: AppleCLCD 1080x2400 stride 4320 at 0x9c000000, default surface 1`, init alive, no panic. Phone image **`shim/out/shim-boot-0046n.img`** (SHA256 9c4d2fe9..., CI `39024108588` with the review fixes: swap bounds check, zeroed 64-bit async ref, port release, 1.5 GiB wired budget, ref leak/race fixes; QEMU re-checked) = 0046 kernel + `shim/out/sweet-0046hi.adt` + the 0045n cmdline; boot it on image v8 (backboardd/SpringBoard log to console) and film. Expected new console lines: `SWEET SURF: <proc> create id ...`, `SWEET FB: backboardd sel N ...`, `SWEET FB: swap ...`. Open question for the next wall: QuartzCore's IOMFB server builds its renderer from Metal first (`CAMetalContextCreate`), GLES only when enabled; how the CPU renderer gets selected on a device without a GPU is not yet established.
- **IOSurface values ABI (offline RE, `/run/media/dipa/android/ios-sweet-work/iosurface-values.md`) - TODO in SweetSurface (0046 only accepts and drops values, so IOSurfaceCopyValue always returns NULL):** sel 9 SetValue in = {u32 id, u32 pad, IOCFSerialize([value, key]) or ([dict] = merge)}, sel 0xb RemoveValue in = {u32 id, u32 pad, key\0} (empty key = remove all); both out 4 bytes = new generation, client accepts only (gen+2)|1. Kernel after each change: gen = (gen+2)|1 (odd, never 0) -> state+0x20, serialized size (>=1) -> state+0x28. sel 0xa in {u32 id, u32 0, u8 0}, out {u32 ?, u32 gen, serialized non-bulk dict}; too small -> 0xe00002db + needed size (client retries x16). sel 0x1b in 0x88: bulk struct 0x70 @0, u64 valid size @0x70, u64 changed mask @0x78, u32 id @0x80 -> copy masked fields into state+0x30 (bit0 32B @0, bit1 16B @0x20, bit2 8B @0x30, bits3-10 1B @0x38..0x3f, bits11-14 24B @0x40/4B @0x58/8B @0x5c/1B @0x64).
- **IOMFB display matching confirmed (offline RE, `/run/media/dipa/android/ios-sweet-work/iomfb-match.md`):** the framework never matches on "AppleCLCD"; any registered IOMobileFramebuffer subclass works. `iomfb_match_callback` reads only `dfr`/`AppleTV`/`external` (CFBoolean, service itself, no parents); internal main display = all absent/false (type 0, name "primary"). Display count = /arm-io children whose device_type starts with "display-subsystem" (count 0 -> CreateDisplayList returns NULL; more nodes than services -> 30 s wait). IOMobileFramebufferOpen fails only on IOServiceOpen failure; canvas-width/height read as 4-byte CFData from the IOService-plane parent (optional). CopyProperty = IORegistryEntrySearchCFProperty on the service only. Patch 0046 (disp0 node, `external`=false, AppleCLCD : IOMobileFramebuffer) fits all of this.
- **IOMobileFramebuffer swap + notification ABI (2026-10-17, offline).** Swap record = fb+0x18, **0x46c bytes**, zeroed by SwapBegin and sent whole by `kern_SwapEnd` = IOConnectCallStructMethod(sel 5, rec, 0x46c, no output). **SwapBegin** = sel 4, no input, 1 scalar out = swap id (stored at rec+0x50). `kern_SwapSetLayer(fb, layer<4, IOSurfaceRef, CGRect a, CGRect b, flags)`: rec+0x54+4*layer = **IOSurface id**; rec+0x104 bit layer = layer enabled (rec+0x108 bit cleared); rect a (int x,y,w,h, scaled) at rec+0x64+16*layer, rect b at rec+0xc4+16*layer; rec+0x114+4*layer = transform from flags&0xf; flag bits 5/31/6/7/8/9 set bytes rec+0x2ca/0x2cc/0x2e3/0x2e5/0x2e6/0x467+layer. A NULL surface only sets the enable bit with zero id. SwapWait = sel 6 scalars [swap id, timeout, 0].
  - **Notifications**: `IOMobileFramebufferScheduleWithDispatchQueue`/`GetRunLoopSource` create an IONotificationPort and `IOConnectSetNotificationPort(conn, type, port, 0)` (kernel `registerNotificationPort`). `kern_EnableNotifications(fb, type, cb, ctx)` = **sel 72 scalars [NotifyCallbackFuncs[type], fb, type, 0]** -> the kernel keeps an async reference {port, func, refcon=fb} per type and fires it with `sendAsyncResult64`. Types: 0 HotPlug, 1 Power, 3 FrameInfo (args[0] = mask of 31-bit keys, args[1] u32, then values), 4 CRC, **5 Vsync**: 6 args, each a 32-bit half in a u64 slot: (ts lo, ts hi), (t2 lo, hi) passed through the time-ingest helper, (t3 lo, hi); the framework then calls the client's vsync callback(fb, ts, t2', t3, ctx). Vsync callbacks are dropped while the notification port has queued messages.

- **IOSurface.framework user-client ABI reversed (2026-10-17, offline, step 2 of the GUI plan).** `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image IOSurface` (selector scan script: scratchpad `selscan.py`).
  - Connect (`_iosConnectInitalize`, pthread_once): `IOServiceGetMatchingService(IOServiceNameMatching("IOCoreSurfaceRoot"))`, retried with sleep(1) up to 241 times (a missing service stalls every client ~4 min, no crash); `IOServiceOpen(type 0)`; then **sel 13** (no inputs, struct out 0x18 bytes = `_ioSurfaceLimits`) and requires u16 at out+0x16 == 1 (ABI version); out+0 = offset/plane-base alignment mask, out+4 = bytes-per-row alignment mask (used as (x+m)&~m), +0..+0x14 also copied into IOSurface remote-method init, otherwise logs and closes the connection.
  - **Create = sel 0**: scalar in [parent id or 0], struct in = `IOCFSerialize(props, kIOCFSerializeToBinary)` (OSUnserializeBinary format; keys IOSurfaceWidth/Height/BytesPerRow/BytesPerElement/PixelFormat/AllocSize/PlaneInfo/CacheMode/IsGlobal/...), struct out **0xa68 bytes** ("lock result"). **Lookup = sel 4**: scalar in [id], same struct out. LookupFromMachPort = sel 0x22 (scalar in [port name]); CreateMachPort = sel 0x23 (scalar in [id, options], scalar out [port name]).
  - Lock result (copied to client+0x68, size 0x68 + planes*0x80, min 0xe8): 0x00 u64 base address **mapped in the caller's task**; 0x08 u64 task VA of a per-surface shared state page (+0 u64 registry id, +8/+0xa u16 bound accel ids, +0xc u32 seed, +0x14 u8 tiled, +0x20 u32 value generation, +0x24 YCbCr matrix, +0x28 u32 non-bulk values size, +0x2d u8 displayable, +0x2e u8 sysmem-only, +0x30 0x70 bytes bulk attachments); 0x10 u64 task VA of timestamp page (4 u64 indexed timestamps, +0x20 detach code); 0x18 u32 surface id; 0x1c u32 alloc size; 0x20 width; 0x24 height; 0x28 bytes per row; 0x2c buffer offset; 0x30 pixel format; 0x34 u32 (dcache flush length); 0x38 plane count; 0x40 u16 bytes/element; 0x42 u8 element width; 0x43 u8 element height; 0x44 cache mode; 0x4c u8 subsampling; 0x4d u8 prohibit-use count; 0x50 parent id; 0x54 slice count; 0x58 u64 trace id; 0x60 u64 protection options; planes[n] at 0x68+n*0x80 (+0 width, +4 height, +8 bytes/row, +0xc offset, +0x14 size, +0x18 u16 bpe, +0x1a/+0x1b u8 element w/h, +0x1c u8 component count, +0x1d address format, +0x54 u8 compression type (non-zero -> no CPU base address)).
  - **Traps** (IOConnectTrapN -> `IOUserClient::getTargetAndTrapForIndex`): 0 IncrementUseCount(id, category), 1 DecrementUseCount(id, category), 2 **Lock**(id, options, &seed_out), 3 **Unlock**(id, options, &seed_out), 4 Release(id), 5 Release after a failed create/lookup setup (id).
  - Other selectors: 5 SetYCbCrMatrix, 6 WrapClientImage, 7 WrapClientMemory, 9 SetValue (serialized), 0xa UpdateNonBulkValueCache (struct in 9), 0xb RemoveValue, 0xc BindAccel, 0x11 SetSurfaceNotify (async), 0x12 RemoveSurfaceNotify, 0x13 Log, 0x14 SetPurgeable, 0x15 SetOwnership, 0x16 SetTiled, 0x18 SetTimestamp, 0x19 GetTileFormat, 0x1a CopyDataValueBytes, 0x1b SetBulkAttachments (struct 0x88), 0x1e/0x2e-0x31 (via outlined helpers), 0x1f SetCompressedTileDataRegionMemoryUsed, 0x20 GetGraphicsCommPageAddress, 0x21 SetIndexedTimestamp, 0x24-0x26/0x2d IOSurfaceAccelerator, 0x27-0x29 shared events, 0x2a SignalEvent, 0x2b Set/InitDetachModeCode, 0x2c SetOwnershipIdentity, 0x32-0x34 data properties.
  - => SWEET kernel service: class/name **IOCoreSurfaceRoot** + IOSurfaceRootUserClient; minimum = sel 13, 0, 4, 9/0xa/0xb (values), traps 0-5, 0x22/0x23 later for cross-process surfaces (CA sends surfaces to backboardd by mach port). Memory: IOBufferMemoryDescriptor per surface, mapped into each task with createMappingInTask; ids from a global table.

- **Image v8: daemon logs on the console.** `tools/patch-launchd-plist.py IN OUT LABEL...` rewrites launchd.plist (binary, plistlib): renames every `_PanicOnCrash` to `_PanicOnCrasX` and gives the listed jobs `StandardOutPath`/`StandardErrorPath` `/dev/console` (devfs console is 0622, writable by mobile) plus `OS_ACTIVITY_DT_MODE=YES` (os_log mirrored to stderr) and `CFLOG_FORCE_STDERR=1`. v8 = v7 + that plist for com.apple.backboardd and com.apple.SpringBoard, written through the mount (796310 bytes, root:80 0644), SHA256 in `ios16-root-20H392-v8.img.sha256`, `.simg` ready; boot with `shim/out/shim-boot-0045n.img`. Goal: see backboardd's uncaught exception text and the window server's display probing. ODDITY (unresolved): the v5 raw-image rename at offset 0x1e025f000 is present in the v5-v7 image bytes, but the plist read through a Linux mount of v7 still had the original `_PanicOnCrash` keys; filefrag shows the file as one extent. Never patch file contents through raw offsets again; write through the mount.
- **IOMobileFramebuffer.framework reversed (step 1 of the GUI plan).** `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image IOMobileFramebuffer`.
  - Display discovery (`IOMobileFramebufferCreateDisplayList` -> `getDisplayListNumber`): iterates children of `IODeviceTree:/arm-io`, counts nodes whose `device_type` is "display-subsystem" or "ext-display-subsystem" (or `compatible` "paravirtualizedgraphics,gpu"); then `iomfb_populate_display_infos` adds an IOServiceAddMatchingNotification(IOServiceFirstMatch, **IOServiceMatching("IOMobileFramebuffer")**) and runs the run loop up to 30 s until that many services matched. `iomfb_match_callback` reads service properties `dfr`, `AppleTV`, `external` (CFBoolean) and names displays (external ones "%s-%d").
  - `IOMobileFramebufferOpen(service, task, type, &fb)`: `__ioMobileFramebufferAlloc` (CFPreferences com.apple.iokit.IOMobileGraphicsFamily: canvas_width/height, override_display_width/height, override_panel_width/height, benchmark, enable_ktrace), `IOServiceOpen(service, task, type)` (GetMainDisplay passes type 0), `getEDTProperty` reads `canvas-width`/`canvas-height` from the service's IODeviceTree parent, then fills a table of `kern_*` function pointers.
  - User client selectors (`kern_*` -> IOConnectCall*): 3 _kern_GetLayerDefaultSurface[ScalarMethod_stub]; 4 _kern_SwapBegin[ScalarMethod_stub]; 5 _kern_SwapEnd[StructMethod_stub]; 6 _kern_SwapWaitWithTimeout[ScalarMethod_stub] _kern_SwapWait[ScalarMethod_stub]; 7 _kern_GetID[ScalarMethod_stub]; 8 _kern_GetDisplaySize[ScalarMethod_stub]; 10 _kern_SetTVOutMode[ScalarMethod_stub]; 11 _kern_SetWSSInfo[ScalarMethod_stub]; 12 _kern_RequestPowerChange[ScalarMethod_stub]; 13 _kern_EnableStatistics[ScalarMethod_stub]; 14 _kern_SetFlags[ScalarMethod_stub]; 15 _kern_SetDebugFlags[ScalarMethod_stub]; 16 _kern_SetTVOutSignalType[ScalarMethod_stub]; 17 _kern_SetGammaTable[StructMethod_stub]; 18 _IOMobileFramebufferIsMainDisplay[ScalarMethod_stub]; 19 _kern_SetWhiteOnBlackMode[ScalarMethod_stub]; 20 _kern_SwapSignal[ScalarMethod_stub]; 22 _kern_SetDisplayDevice[ScalarMethod_stub]; 23 _kern_SetDigitalOutMode[ScalarMethod_stub]; 24 _kern_GetHDCPDownstreamState[StructMethod_stub]; 25 _kern_GetDigitalOutState[ScalarMethod_stub]; 26 _kern_printDisplayRegs[ScalarMethod_stub]; 27 _kern_GetGammaTable[StructMethod_stub]; 28 _kern_GetDotPitch[ScalarMethod_stub]; 29 _kern_GetDisplayArea[StructMethod_stub]; 30 _kern_EnableDisableDithering[ScalarMethod_stub]; 31 _kern_SetUnderrunColor[ScalarMethod_stub]; 33 _kern_EnableDisableVideoPowerSavings[ScalarMethod_stub]; 34 _kern_SetVideoDACGain[ScalarMethod_stub]; 35 _kern_SetLine21Data[ScalarMethod_stub]; 41 _IOMobileFramebufferEnableMirroring[ScalarMethod_stub]; 42 _IOMobileFrameBufferGetMirroringCapability[StructMethod_stub]; 43 _IOMobileFramebufferSetRenderingAngle[StructMethod_stub]; 44 _IOMobileFramebufferSetMirrorContentRegion[StructMethod_stub]; 47 _kern_HDCPSendRequest[ScalarMethod_stub]; 48 _kern_HDCPGetReply[ScalarMethod_stub]; 49 _kern_SurfaceIsReplaceable[ScalarMethod_stub]; 50 _kern_SetBrightnessCorrection[ScalarMethod_stub]; 51 _kern_SetColorRemapMode[ScalarMethod_stub]; 52 _kern_SwapCancel[ScalarMethod_stub]; 53 _IOMobileFramebufferSetCanvasSize[ScalarMethod_stub]; 54 _IOMobileFramebufferGetMatrix[Method_stub]; 55 _IOMobileFramebufferSetMatrix[Method_stub]; 56 _IOMobileFramebufferKernelTests[StructMethod_stub]; 57 _kern_GetColorRemapMode[ScalarMethod_stub]; 66 _kern_SPLCSetBrightness[ScalarMethod_stub]; 67 _kern_SPLCGetBrightness[ScalarMethod_stub]; 68 _kern_SetParameter[Method_stub]; 69 _kern_SwapSetColorMatrix[StructMethod_stub]; 72 _kern_DisableNotifications[ScalarMethod_stub] _kern_EnableNotifications[ScalarMethod_stub]; 73 _kern_ChangeFrameInfo[ScalarMethod_stub]; 74 _kern_SupportedFrameInfo[Method_stub]; 75 _kern_FactoryPortal[StructMethod_stub]; 77 _kern_GetCurrentAbsoluteTime[ScalarMethod_stub]; 78 _kern_SetBlock[Method_stub]; 79 _kern_GetBlock[Method_stub]; 80 _kern_GetLinkQuality[ScalarMethod_stub]; 81 _kern_SwapCancelAll[ScalarMethod_stub]; 82 _kern_GetProtectionOptions[ScalarMethod_stub]; 83 _kern_CopyLayerDisplayedSurface[ScalarMethod_stub]; 84 _kern_SetContrast[StructMethod_stub]; 85 _kern_GetBufBlock[Method_stub]; 86 _IOMFBGainEncoderFinishEncoding[Method_stub]; UNKNOWN {}
  - => Kernel needs: an `/arm-io` child node with device_type "display-subsystem" (+ canvas-width/height) and an IOService of class **IOMobileFramebuffer** (subclass name match) attached under it, opened with type 0, implementing at least GetDisplaySize(8), IsMainDisplay(18), GetID(7), GetLayerDefaultSurface(3), SwapBegin(4)/SwapEnd(5 struct)/SwapWait(6), Enable/DisableNotifications(72), frame info(73/74), CopyLayerDisplayedSurface(83), plus IOSurface for the swapped buffers. NEXT: CoreAnimation's AppleDisplay/IOMFBDisplay usage of these (constructor, first swap, vsync), then IOSurface.framework's IOSurfaceRoot selectors.
- **GUI PLAN (decided 2026-10-16): CPU rendering + kernel IOMobileFramebuffer.** User: CPU rendering is fine for now (goal = prove the GUI runs), may later research an Apple-style GPU driver for the Adreno 618 -> keep display output and renderer separable. QuartzCore findings (symbols from the cache's .symbols subcache: `ipsw dyld symaddr research/dsc/dyld_shared_cache_arm64 --image QuartzCore`; strings: `ipsw dyld macho ... QuartzCore --strings`):
  - Renderers: `sw_new_context` (CA::OGL::SWContext, full CPU renderer incl. blur, images, IOSurface-backed surfaces, make_buffer_current(WindowServer::Surface)), `gles_new_context`, `metal_new_context`, `new_null_context`. Env knobs include CA_ENABLE_OGL, CA_DISPLAY_TYPE, CA_FORCE_LOCAL_SERVER, CA_FORCE_TIMER, CA_CANVAS_WIDTH/HEIGHT, CA_MAIN_DISPLAY_SCALE/ORIENTATION, CA_DISABLE_RENDER, CA_ALWAYS_RENDER (selection logic not traced yet).
  - `-[CAWindowServer _detectDisplays]` (0x1884e3150) iterates static tables `open_funcs`/`count_funcs` = AppleCLCDDisplay, AppleRGBOutDisplay, AppleWirelessDisplay only; each `count()` = `display_count_of_type(IOMFBDisplayType)` over **`IOMobileFramebufferCreateDisplayList()`**, `open(i)` = `create_display_of_type` -> `CA::WindowServer::AppleDisplay(CFString name, ..., IOMFBDisplayType)` (an IOMFBDisplay driven by IOMFBServer: vsync_callback, frame_info_callback, swaps). `CA::WindowServer::VirtualDisplay` exists but is never auto-detected (explicit API only). => the main display MUST come from an IOMobileFramebuffer kernel service.
  - NEXT: reverse IOMobileFramebuffer.framework: IOMobileFramebufferCreateDisplayList / IOMobileFramebufferOpen (service matching, display type property), the user-client selectors used by IOMFBServer (display size/modes, swap begin/set-layer/end with IOSurface ids, vsync notifications), then the IOSurface kernel side (IOSurfaceRoot user client: create/lookup/lock, memory mapping) that both IOMFB swaps and CA surfaces need. Kernel: SWEET IOMobileFramebuffer service that copies the swapped IOSurface to the 1080x2400 framebuffer at 0x9c000000.
- **logd fixed; backboardd = DISPLAY WALL (boot 0045n on v7, 21:08:57 UTC, frames VID_20261016_230850 00:55-01:28, slide 0x4c3ec000, `research/crash-0045n-v7.txt`).** No `CRASH logd` any more; new daemons run (runningboardd, WirelessRadioManagerd, networkserviceproxy, dasd, cloudpaird, magicswitchd, atc, askpermissiond, ManagedSettingsAgent, containermanagerd uses AKS 0/17). New: locationd sig 11 at CFRunLoopAddSource+132 (NULL source) from its main+0x2af138 in a dispatch_once. **backboardd** sig 6: abort <- std::terminate <- _objc_terminate <- dispatch_once <- main+0x9334 = the "start %{public}@..." wrapper (0x100009264) for **"window server"** (block 0x10000a770 -> dispatch_once body 0x10001d7f0 = StartWindowServer): MTLSetShaderCachePath, `[CAWindowServer serverWithOptions:@{kCAWindowServerDisableUpdatesOnMainDisplay: @YES}]`, `setRendererFlags:`, **`mainDisplay`** -> `displayId` -> `[CADisplay displayWithDisplayId:]`, setWindowServerDisplay:, bounds, pointScale, currentMode, preferredScale, nativeOrientation, touchScales... With no display, mainDisplay is nil and it throws. (HID system and GS start fine before it.) SpringBoard dies on the same missing display (FBSDisplayMonitor). QuartzCore display backends (from the cache's .symbols subcache, `ipsw dyld str`): `CA::WindowServer::AppleCLCDDisplay` (IOMobileFramebuffer hardware) and **`CA::WindowServer::VirtualDisplay`** (open(), new_server, clone_update). `CA_DISPLAY_TYPE` and `CA_FORCE_LOCAL_SERVER` strings exist in QuartzCore but have no direct xref (likely read via a table of CA_* env names). NEXT: find how CA::WindowServer::Server enumerates displays (IOMobileFramebuffer services vs VirtualDisplay / CA_DISPLAY_TYPE) and choose: (a) kernel IOMobileFramebuffer service + IOSurface, or (b) a VirtualDisplay rendered by CA's CPU path (CA::OGL::SW) and copied to the framebuffer.
- **watchdogd + CommCenter + identityservicesd fixed (boot 0045n on v6, 20:41:30 UTC, frames VID_20261016_224133 00:39-01:13, slide 0x20fec000).** `SWEET WDT: watchdogd sel 0 in 0/0 out 1/0 -> ok`, no watchdogd/CommCenter/identityservicesd crashes (CommCenter/identityservicesd now call AKS 0/17/7). usermanagerd boot task runs (UMD_INIT creates primary session uid 501 "mobile", personas 99 System and 199 Default registered with the kernel); `Failed to atomically swap writing file /private/var//keybags/usersession.kb: Operation not supported (45)` (HFS lacks the atomic swap rename; non-fatal so far). Remaining: SpringBoard (FBSDisplayMonitor, no display), backboardd (uncaught exception), mediaserverd, lockdownd (crash inside obfuscated code, main+0x4c1b4?), logd. **logd**: main+0x18160 = `BUG IN LIBTRACE: Failed to migrate directory` from 0x10001801c(dir 0): 0x100016538 requires the dir to exist with uid/gid/mode from the table at 0x10002df14 (0: /private/var/db/diagnostics 272:272 0751, 1: /private/var/db/uuidtext 272:272 0755, 2: /private/var/db/diagnostics/timesync 272:272 0755) plus a `.migrated` file, else XPC "operation 6" to a helper and crash. **Image v7** = v6 + those dirs/markers (also in mkiosroot.sh), SHA256 in `ios16-root-20H392-v7.img.sha256`, `.simg` ready. Boot with `shim/out/shim-boot-0045n.img`.
- **Exit-reason text works (boot 0044n, frames VID_20261016_221726 00:32-00:53, slide 0x22d5c000).** CommCenter/identityservicesd: `couldn't dlopen libobjc-trampolines.dylib: dlopen(/usr/lib/libobjc-trampolines.dylib, 0x0106): tried: '/usr/lib/libobjc-trampolines.dylib' (no such file, not in dyld cache)`: the file only exists in the OS cryptex and dyld does not search cryptexes at ignition_level=1. 19 cryptex files have no root counterpart (OS: DriverKit dyld cache + .symbols, VisualTestKit, libffi-trampolines, libobjc-trampolines, libstdc++ 6.0.9 + 2 symlinks; App: SafariSupport.bundle, AuthenticationServicesAgent, com.apple.Safari.History, passwordbreachd, safarifetcherd, webbookmarksd, webinspectord, webpushd) -> hard-linked (symlinks copied: Linux hfsplus cannot hard-link symlinks); `tools/mkiosroot.sh` does it generically. watchdogd still crashed: the `-wdt_no_pmu` / `/arm-io/wdt no-pmu` check (0x10000a01c) only runs when os_variant_has_internal_diagnostics; otherwise 0x100009b18 looks up IOServiceMatching("IOService") + IOPropertyMatch {IOPMUPrimary: 1} (NSConstantDictionary) and crashes if absent, then IORegistryEntrySetCFProperty(boot stage 0xff) (failure only logged). Patch **0045**: IOWatchdog sets IOPMUPrimary = 1 and accepts setProperties; CI `38961814194` -> `xnu/out-0045`. **Image v6** = v5 + the 19 cryptex links, SHA256 7c610c6a...297a, `ios16-root-20H392-v6.simg` (full flash needed). Boot image `shim/out/shim-boot-0045n.img` (0045 + sweet-0044hi.adt). Still open: SpringBoard (no display), backboardd (uncaught exception, reason none), mediaserverd (Fig NULL dict), logd (main+0x18160), lockdownd (main+0x4c1b4).
- **System survives daemon crashes (boot 0043p, video frames VID_20261016_215006 00:25/00:42/00:54).** With the v5 plist patch no panic: launchd keeps launching (runningboardd, powerd, tccd, healthd, peopled, cryptexd, routined, aksd, mediaremoted, familynotificationd, nanoprefsyncd, navd, cloudpaird, passd, amsaccountsd, accessoryupdaterd, wcd ...). Shared cache slide that boot 0x406b4000 (`research/crash-0043p.txt`). watchdogd still crashed at main+0xb82c from the PMU step: `-wdt_no_pmu` is only honored when os_variant_has_internal_diagnostics; customer builds read `no-pmu` from IODeviceTree:/arm-io/wdt (IORegistryEntrySearchCFProperty) -> mkadt adds /arm-io/wdt {no-pmu}. **cryptexd** sig 6: abort_with_payload <- os_crash_fmt <- `__darwin_arm_secure_boot_chip.cold.7` ("panic: failed to get crypto algorithm") <- `_img4_chip_select_personalized_ap`: reads /chosen use-ddi-secure-boot, allow-ecid-mismatch, crypto-hash-method ("sha1" | "sha2-384"), /chosen/asmb lp-smb0/1 -> mkadt adds crypto-hash-method "sha2-384". **identityservicesd** sig 6 = same `_objc_fatal` in imp_implementationWithBlock as CommCenter (block trampolines; message needed). lockdownd sig 5 at main+0x4c1b4. Patch **0044**: crash report adds `CRASH name reason ns N code X: text` (exit reason description = abort_with_payload text). CI `38959096811` -> `xnu/out-0044`, QEMU OK. Image `shim/out/shim-boot-0044n.img` = 0044 + `shim/out/sweet-0044hi.adt` (wdt no-pmu, crypto-hash-method) + cmdline (wdt=-1, no -wdt_no_pmu).
- **First symbolicated daemon crashes (boot 0043u on journaled v4, 19:38:53 UTC; video frame chat image 36; transcribed in `research/crash-0043u.txt`; shared cache slide 0x40d60000 for every process).** (Gemini's video transcription invented values, use frames only.) `tools/sweet-crash.py research/dsc/dyld_shared_cache_arm64 x research/crash-0043u.txt`:
  - **watchdogd** pc main+0xb82c (`_os_crash` trap helper) from 0x100009bb0 = set PMU boot stage via IORegistry (no PMU) -> fix: boot-args `wdt=-1 -wdt_no_pmu` (Apple's own test mode writes "%s wdt=-1 -wdt_no_pmu"; watchdogd logs "skipping setting PMU boot stage because -wdt_no_pmu found in boot-args or no-pmu found in EDT"). Kernel effect of wdt=-1: sched hygiene debug off, zone_exhausted_timeout -1 (harmless).
  - **SpringBoard** sig 5 in `-[FBSDisplayMonitor _initWithBookendObserver:transformer:]+1160` <- `+[FBDisplayManager sharedInstance]` <- `FBSystemShellInitialize` <- `SBSystemAppMain`: no main display. GUI WALL: display service (IOMobileFramebuffer / CoreAnimation display).
  - **backboardd** sig 6: abort <- std::terminate <- _objc_terminate (uncaught exception; message not shown).
  - **CommCenter** sig 6: `_objc_fatal` in `imp_implementationWithBlock` (from `+[_PFRoutines initialize]`, CoreData): objc block trampolines cannot be allocated -> likely kernel gap (trampoline page remap); will hit many processes.
  - **mediaserverd** sig 11: CFDictionaryGetValue(NULL) in FigNotificationListenerStartNotifications (routing session manager).
  - **logd** sig 5 at its main+0x18160 (bt main+0x9dfc); lockdownd sig 5 (not yet symbolicated).
  - Image v5 = v4 + launchd.plist (`/System/Library/xpc/launchd.plist`, contiguous at image offset 0x1e025f000, 1456980 bytes) with the 7 `_PanicOnCrash` keys renamed `_PanicOnCrasX` in place (raw image patch, no metadata change) -> `diff-v4-v5.simg` = 7 blocks; v5 SHA256 78f96974...185a. Boot image `shim/out/shim-boot-0043p.img` = 0043 + `wdt=-1 -wdt_no_pmu`.
- **0043 console crash reports (QEMU verified); image `shim/out/shim-boot-0043u.img`; NEXT: flash v4 + boot 0043u.** Boot 0042u (video photo IMG_20261016_211646): short exec lines work; watchdogd crashes with NO `SWEET WDT:` line (fails before its first IOWatchdog call: lookup or IOServiceOpen, or elsewhere); lockdownd, SpringBoard, mediaserverd, CommCenter, identityservicesd, backboardd, watchdogd all crash repeatedly ("Too many corpses being created" = corpse limit, no crash reports). AKS callers: lockdownd (0, 7), imagent/sleepd (0, 17, 7), backboardd (0, 17), UserEventAgent (0, 7, 102, 103 -> unsupported). Patch **0043**: `sweet_crash_log` (osfmk/kern/exception.c, called from proc_prepareexit for crash exits on the current proc) prints `CRASH name[pid] sig S code (exc<<32|code) sub X slide SR mh MH`, `CRASH name pc lr sp fp far`, `CRASH name bt` (10 fp frames); AKS sel 103 notify_state_is_set -> 0. CI `38954520419` -> `xnu/out-0043`. QEMU test: init forks, child `brk #1`: `CRASH launchd[2] sig 5 code 0x600000001 sub 0x1000004f0 slide 0x0`, pc correct, parent keeps running (pid 1 crashes panic before proc_prepareexit, so test with a child). `tools/sweet-crash.py CACHE ROOT [report]` symbolicates typed-in CRASH lines (`ipsw dyld a2s` with addr - slide; main binary offsets = addr - mh + 0x100000000).
- **v3 reflashed 18:50-18:55 UTC (`research/flash-userdata-v3b.log`, 24/24 OKAY); 0042u booted 19:01:17 UTC on the clean disk (`research/boot0042u-2.log`), SLOW MO VID pending (watchdogd failure reason).** ABL hangs on the first `fastboot boot` after every big flash; user re-enters fastboot. User gave standing approval to reflash/boot without asking (memory standing-flash-approval). Commits now end with `Co-Authored-By: dipa-studio <183933817+dipa-studio@users.noreply.github.com>` (user request; never a Claude trailer).
  - watchdogd flow: connect_to_kext (0x100005408): IOServiceGetMatchingService("IOWatchdog") fails -> "failed to discover" + _os_crash; IOServiceOpen(type 1) fails -> "IOServiceOpen failed with error : 0x%x" + _os_crash. Then sel 0 (out 1 scalar): 0 -> "userspace monitoring disabled", 0x100009bb0, sleep 2, exit(0); nonzero -> "userspace monitoring enabled", normal operation.
  - **Image v4 (JOURNALED):** `tools/mkiosroot.sh` now does `mkfs.hfsplus -J`, mounts with `-o loop,force`, adds the /System/Library/Caches/com.apple.dyld hard links (44) and /private/var/keybags/systembag.kb (0700/0600 root). Built from the IPSW dmgs (OS 087-86698-044, SystemOS 087-86593-047, AppOS 087-86715-047) -> `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v4.img` SHA256 fba4aeae...ec0f9 + `.simg`. Header: attr 0x80002100 (unmounted, journaled), journal info block 129, journal 8 MiB at 532480 flagged need-init. Linux `fsck.hfsplus -n` reports "Volume header needs minor repair" on any fresh journaled volume even after -y (quirk). QEMU: 64 MB journaled test root (`rd=md0 rootrw=1`, 0042 kernel): `hfs: Initializing the journal (joffset 0x3000 sz 0x80000)` -> mounted -> init runs, no panic. NEXT: flash v4 (full), boot 0042u.
- **SPRINGBOARD STARTS (boot 0041u 18:39:53 UTC, photo IMG_20261016_204142).** backboardd, bluetoothd, fairplayd.H2, SpringBoard (pid 111, crashed: "Too many corpses"), xpcproxy run; `SWEET AKS: backboardd sel 0 -> 0`, `sel 17 in 1/0 out 0/4096 -> 0`. Panic: watchdogd[113] exited, namespace 2 subcode 5 (SIGTRAP = its _os_crash): watchdogd crashes on purpose when IOServiceGetMatchingService("IOWatchdog") fails ("connect_to_kext() unexpectedly failed") or IOServiceOpen(type 1) fails ("IOServiceOpen failed with error"); IOWatchdog DOES register (QEMU msgbuf: `SWEET WDT: IOWatchdog registered`), cause not on screen yet -> need video. Note `wdt_test=no_user_checkin` makes watchdogd log "detected testing boot-args to not run, exiting" (path not reached here?). **HFS CORRUPTION:** `hfs_swap_BTNode: offset #0 invalid (0xBC1D) (blockSize 0x2000 numRecords 81)`, `node=19677 fileID=4` (catalog), `hfs_mark_inconsistent` repeated. Likely cause: non-journaled HFS + unclean panics while writing (0038e wrote a 2.7 GB core then panicked; every boot since ends in panic). Plan: reflash v3 (clean), longer term HFS journaling. Patch **0042**: one short `exec NAME` console line instead of the 3-line "Allowing spawn of iOS binary" notice; CI `38949451276` -> `xnu/out-0042`; image `shim/out/shim-boot-0042u.img` (same cmdline as 0041u).
- **LAUNCHD DAEMONS RUN (boot 0039u, 18:29:13 UTC, photo IMG_20261016_203052).** With `launchd_unsecure_cache=1` all boot tasks pass and launchd starts LaunchDaemons (pids > 100: identityservicesd 114 and lockdownd 106 crash, "Too many corpses being created"). Fatal: `watchdogd: ERROR: failed to discover watchdog KEXT service` -> exit (namespace 2 = signal, subcode 5) -> `_PanicOnCrash` panic. watchdogd: IOServiceMatching("IOWatchdog"), IOServiceOpen type 1, IOConnectCallScalarMethod sel 0/1 (check in)/3/4 (disable/enable userspace monitoring)/5, IOConnectCallStructMethod sel 2 (1 KiB in) and 9 (small out); VM path ("detected virtual machine environment and no watchdog KEXT found, exiting...") only when it detects a VM. Console also flooded with `hfs: set hardlink bit on vol=iOSRoot cnid=321318` (Linux-made hard links lack kHFSHasLinkChainBit; repaired only in memory on each lookup). Patches **0040** (`iokit/Kernel/arm/SweetWatchdog.cpp`: IOWatchdog + IOWatchdogUserClient, all selectors succeed with zeroed outputs, each logged once as `SWEET WDT: ...`) and **0041** (sweet_hfs hfs_catalog.c: the three link-repair printfs limited to 8 per boot); CI `38948245372` PASSED -> `xnu/out-0041` (QEMU regression OK). Image `shim/out/shim-boot-0041u.img` (0041 + sweet-0038hi.adt + ufsrw rootrw + launchd_unsecure_cache=1) booted 18:39:53 UTC (`research/boot0041u.log`), photo pending.
- **v3 FLASHED + keybag passes; next wall AMFI (launchd_cache_loader).** User said "flash, nothing to lose": `fastboot -S 512M flash userdata ios16-root-20H392-v3.simg` 17:51:52-17:57:01 UTC, 24/24 chunks OKAY (`research/flash-userdata-v3.log`). userdata = v3 (SHA256 fa84274c...22df) until the next rw boot. ABL fastboot then hung ("Sending" forever, `reboot bootloader` timed out) until the user re-entered fastboot by hand (common Xiaomi ABL crash). Boot 0038e 18:06:15 UTC (`research/boot0038e-3.log`), photos IMG_20261016_200812/200838: keybag OK, then boot tasks tzinit (`Bad zoneinfo link`, resets to system partition, OK), finish-restore, finish-demo-restore, sysstatuscheck, prng_seedctl (`failed to load kernel prng seed`, `failed to load virtual random (-147)`, AllowCrash), auearlyboot, then **launchd_cache_loader: `abort: Unable to find AMFI`** -> 2.7 GB core written to /cores in 91 s -> launchd panic `launchd_cache_loader[22] exited -- exit reason namespace 7 subcode 0x1`. launchd_cache_loader: SecStaticCodeCheckValidity of /System/Library/xpc/launchd.plist with detached .sig, then IOServiceMatching("AppleMobileFileIntegrity") + IOServiceOpen type 0 + IOConnectCallMethod sel 6 (1 scalar = 1, struct in = cdhash) = trust the cdhash, then sends the cache to launchd. Boot-arg `launchd_unsecure_cache=1` skips signature + AMFI ("Using unsecure cache"); the value is parsed with strtoul base 10 (helper 0x100002da8), so a path = 0 = off: boot 0039w (18:17:13 UTC, `=/System/Library/xpc/launchd.plist`, photo IMG_20261016_202008) still aborted `Unable to find AMFI` (core dump now skipped: `Failed to generate core file ... error 14`, so 0039 works). Image `shim/out/shim-boot-0039u.img` uses `launchd_unsecure_cache=1`. Patch **0039**: do_coredump = 0 on SWEET (kern.coredump sysctl still works); CI `38945267341` -> `xnu/out-0039` (_do_coredump now in __common). Image `shim/out/shim-boot-0039w.img` = 0039 + sweet-0038hi.adt + ufsrw rootrw + `launchd_unsecure_cache=/System/Library/xpc/launchd.plist`. TODO later: real AppleMobileFileIntegrity IOService (sel 6 trust cdhash etc.).
- **Image v3 ready, awaiting user "flash".** Boot 0038w 17:38:10 UTC, photo (chat image 30): `SWEET AKS: keybagd sel 0 -> 0x0`, `sel 14 out 1/0 -> 0x0` (x2), `MKB_INIT: mount is with NO CPROTECT ... does not support Data Protection`, `System Keybag loaded`; then keybagd still opens /private/var/keybags/systembag.kb (0x100012d3c, for BackupKeyBagKeys) -> ENOENT, `no-effaceable-storage` not set -> `Can't load the keybag. tears in rain... Time to die` -> `FATAL KEYBAG ERROR: kb_load` -> reboot -> Halt/Restart Timed Out panic. Fix: ADT `/defaults/no-effaceable-storage` (mkadt.py; `shim/out/sweet-0038hi.adt`, `research/q0038-hi.adt`, QEMU OK) + file `/private/var/keybags/systembag.kb` (0600 root, dir 0700; XML plist {KeyBagKeys: data}). **v3 image** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v3.img` = v2 + that file, fsck OK, SHA256 fa84274c...22df; `ios16-root-20H392-v3.simg` (img2simg: zero blocks become FILL chunks, so a full flash overwrites every block the rw boots changed). Flash: `fastboot -S 512M flash userdata ios16-root-20H392-v3.simg`, then boot `shim/out/shim-boot-0038e.img` (0038 + sweet-0038hi.adt + ufsrw=1 rootrw=1).
- **0038 AppleKeyStore (CI 38938744130 PASSED -> `xnu/out-0038`; QEMU msgbuf: `SWEET AKS: AppleKeyStore registered (no passcode, unlocked)`; phone image `shim/out/shim-boot-0038w.img` booted 17:38:10 UTC, `research/boot0038w.log`, photo pending).** QEMU full kernel log trick (fb.txt is only the last screen): `llvm-nm KERNEL | grep _msgbufp` -> `--hmp "x /1gx ADDR"` gives struct msgbuf address (static, 0xfffffe0007b56678 on 0038) -> `--hmp "x /3gx STRUCT"` gives bufc (3rd quad) -> `--hmp "memsave BUFC 0x20000 \"FILE\""` (quote the file name), `tr -d "\0" < FILE`. Same inputs give the same addresses. Boot 0037w 17:08:35 UTC, photo IMG_20261016_191052: bindfs fixed mount; mount-phase-1/2 pass; `cc_fips_test` boot task: all corecrypto FIPS POST tests PASSED in userspace; then keybag boot task `keybagd --init`: `MKB_INIT: FATAL KEYBAG ERROR: failed to load system bag`, `Could not get options entry from the device tree` (x2, IODeviceTree:/options = NVRAM, non-fatal), `REBOOTING INTO RECOVERY MODE` -> reboot -> panic `Halt/Restart Timed Out @IOPlatformExpert.cpp:884` (no restart path on SWEET).
  - keybagd (static libaks): load_devicebag (0x100012c30) calls aks_get_system (sel 14, 0-1 scalar in, 1 out) and loads /private/var/keybags/systembag.kb only if the result is 0xe00002f0 (NotFound); any other error -> fatal; SUCCESS -> skip the file (userspace-reboot path). systembag.kb is a plist {KeyBagKeys}; decrypted with effaceable storage unless IODeviceTree:/defaults has `no-effaceable-storage`. Image has no /private/var/keybags. has_data_protection: statfs of /private/var; no cprotect on our HFS -> device-bag volume mapping skipped.
  - libaks connection: IORegistryEntryFromPath / IOServiceMatching("AppleKeyStore"), IOServiceOpen type 0, then selector 0 (no args) must succeed.
  - **AppleKeyStore selector map (iOS 16.7 AppleKeyStore.framework, via `ipsw dyld disass`):** 0 open, 2 create_bag, 3 save_bag, 4 unload_bag, 5 set_system_with_passcode, 6 load_bag, 7 get_lock_state (1 in, 1 out; bit 2 = unlocked since boot), 9 unlock_device, 10 wrap_key, 11 unwrap_key, 12 unlock_bag/test_stashed_kek, 13 lock_bag, 14 get_system, 15 change_secret_se, 16 internal_state, 17 get_device_state (1 in, struct out <=4K: DER SET of SEQUENCE{UTF8 key, INTEGER}: ss state, sls lock_state (MKBGetDeviceLockState returns it), sb backoff, sbo, sfa failed attempts, sfao, sgs generation, sas assertions, sgpe grace, srcd countdown, sr reserved), 18 recover_with_escrow_bag, 19 obliterate_class_d, 20 drain_backup_keys, 21/22 set/clear_backup_bag, 23 get_bag_uuid, 24 rewrap_key_for_backup, 26/27 assert_hold/drop, 30/31 set/get_configuration, 33-37 stash, 38 auth_token_create, 40 generation, 41 fdr_hmac_data, 42 verify_password, 43 _aks_operation, 44 remote_session, 49/50 signing keys, 51/53/54 stash enable/persist/escrow, 55 unload_session_bags, 57/58 remote peer, 59-62 smartcard, 63 migrate_s_key, 65 set_keybag_for_volume_with_cookie_persona, 66/67 sync bags, 68 copy_volume_cookie_persona, 69-73 se_*, 74-79/84/85/99 fv_* (FileVault/VEK), 80/81 absinthe, 82 make_public_backup_bag, 83 drop_auxiliary_auth, 86 kext get/set options, 87 invalidate_bag, 88-91/94/95/106/107 se_*, 92 lower_iteration_count, 93 get_internal_info, 96-98/117 keybag_persona create/list/delete, 100/101 assert promote/consume, 102/103 notify_state set/is_set, 104 fairplay, 105 change_secret_epilogue, 108 delete_xart_leak, 110-113 backup volume, 114 sealed_hashes_set, 115 prewarm_sps, 118-128 AKSIdentity*/AKSGetLastUser.
  - Patch **0038**: `iokit/Kernel/arm/SweetKeyStore.cpp` (class AppleKeyStore on IOResources, IOUserClientClass AppleKeyStoreUserClient; personality in KernelConfigTables.cpp): 0/4/5/9/12/13/26/27/55/102 success, 14 -> handle 0, 7 -> 0x4, 17 -> DER state (ss 4, sls 0), others kIOReturnUnsupported; logs `SWEET AKS: <proc> sel N arg0 in a/b out c/d -> ret` for every call.
  - Tools: shared cache copied to `research/dsc/` (git-ignored; ipsw needs a writable dir for its .a2s symbol cache); `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image AppleKeyStore|MobileKeyBag`; scratchpad `annot2.py BIN DIS FIXUPS` annotates llvm-objdump output with strings and import names (`ipsw macho info --fixups`).
- **0037 bindfs (phone boot 0037w pending photo).** Boot 0036mw 16:57:47 UTC, photo IMG_20261016_190102: WRITABLE ROOT WORKS: `/dev/ufsroot0 on / (hfs, local, noatime)` after mount_hfs update (GetMasterBlock EBUSY harmless), coredump of mount written to /cores (rw). Then `mount: failed to mount /private/preboot/5CBE3601.../usr/standalone/firmware -> ...: Operation not supported by device (19)` -> exit 74 -> launchd panic `mount[2] exited`. Cause: the macOS-derived config had nullfs but no bindfs (ENODEV = unknown fs type). Caller passes env 0 -> bind not required, ENOENT (missing source dir) tolerated. Patch **0037** adds `bindfs` to FILESYS_BASE in MASTER.arm64.sweet; CI `38936550483` -> `xnu/out-0037` (bindfs_vfsops present; QEMU probe regression OK). Image `shim/out/shim-boot-0037w.img` (0037 + sweet-0036hi.adt + ufsrw=1 rootrw=1) booted 17:08:35 UTC (`research/boot0037w.log`). NOTE: userdata has now been modified by rw boots; it no longer equals the v2 image, so sparsediff with v2 as OLD is not safe any more (full reflash or a new baseline needed).
- **0036 phone: launchd boot tasks run; mount -P 1 needs /chosen/boot-manifest-hash.** Boot 0036hr 16:15:32 UTC, photo IMG_20261016_185236: platform check passes; fsck boot task runs (`fsck: not booting main or diagnostic OS. Skipping fsck on OS container`); mount-phase-1: `failed to get filesystem info` x2 (no IODeviceTree:/filesystems/fstab, non-fatal), `mount: data volume missing, but not required in env: 0`, mount_hfs update of /: `GetMasterBlock: Error 16 opening /dev/ufsroot0` (EBUSY, mounted block dev, non-fatal) then mount() EROFS (read-only boot) -> `mount: / failed with 1`; then `failed to get boot-manifest-hash` -> errx exit 66 -> launchd panic `mount[3] exited`. /sbin/mount: fn 0x100005f90 reads IODeviceTree:/chosen boot-manifest-hash (hex), bindfs-mounts /private/preboot/<HEX>/usr/standalone/firmware (ENOENT tolerated unless required). `tools/mkadt.py` now adds `boot-manifest-hash` = SHA-384("sweet boot manifest") (5CBE3601...5205). ADTs `shim/out/sweet-0036hi.adt`, `research/q0036-hi.adt` (QEMU probe OK, csops 0x26000001). Image `shim/out/shim-boot-0036mw.img` (0036 + new ADT + ufsrw=1 rootrw=1), booted 16:57:47 UTC (`research/boot0036mw.log`): FIRST WRITABLE BOOT of userdata (restore source: v2 image on SSD).
- **0036 CS_SIGNED (phone boot 0036hr pending photo).** Phone boot 0035hr 2026-10-16 15:57:02 UTC (`research/boot0035hr.log`, photo IMG_20261016_180249): highmem works on hardware; shared cache maps (trust-cache warnings only), Apple launchd runs (`Darwin Bootstrapper Version 7.0.0`, `entering ondemand mode`), starts boot task fsck, then userspace panic `boot task is not a platform binary (fsck, /sbin/fsck)`. launchd+0x3fea0: `csops(pid, CS_OPS_STATUS)` must have bit 0x04000000. Cause: nothing set CS_SIGNED (AMFI does it in vnode_check_signature), so csproc_get_blob() returns NULL for every process and csops never reports CS_PLATFORM_BINARY (also breaks per-process cdhash/entitlement queries). QEMU probe init (`csops` status printer, scratchpad csq/) on 0035: `0x02000001`; patch **0036** (`*cs_flags |= CS_SIGNED` in the SWEET AMFI hook), CI `38929635791` -> `xnu/out-0036`: `0x26000001`. Images `shim/out/shim-boot-0036hr.img` / `-0036hw.img` (same cmdlines as 0035). 0036hr booted 16:15:32 UTC (`research/boot0036hr.log`). Next launchd boot tasks (embedded __config plist): fsck -qL and mount -P 1/2 (RequireSuccess); no /etc/fstab on the image.
- **0035 ENTITLEMENTS + PLATFORM BINARIES (QEMU verified).** `xnu/patches/0035-sweet-amfi-entitlements-platform-binaries.patch`: new `iokit/Kernel/arm/SweetEntitlements.cpp` (OSObject subclass: OSDictionary from OSUnserializeXML of the signature's XML entitlements + original XML for CS_OPS_ENTITLEMENTS_BLOB); `bsd/kern/sweet_amfi.c` answers queryEntitlementBoolean/String(+WithProc, string also matches array members), copyEntitlementAsOSObject(+WithProc, retained), asdict (retained), get_xml (kalloc_data copy); built-in MAC policy "SWEET AMFI" (registered from bsd_init before vfs/exec) with mpo_vnode_check_signature: every signed binary on the MNT_ROOTFS mount gets CS_PLATFORM_BINARY (stand-in for AMFI's static trust cache: iOS system binaries are ad-hoc, cd_flags 0x2, platform byte 0), and attaches entitlements ONLY for the writable copy (cs_blob != csb_ro_addr; revalidation passes the RO blob). LESSON: first version attached in adjustContextWithoutMonitor -> QEMU `unable to adjust OSEntitlements context without monitor: 53` because ubc_cs_convert_to_multilevel_hash (4K-page signatures on 16K kernel) sets csb_entitlements_blob = NULL; ALL iOS 16 binaries (launchd, backboardd, SpringBoard) use 4K code pages, so this would have broken launchd on the phone. Boot-arg `sweet_amfi_debug=1` logs `SWEET AMFI: <ident>: N entitlements (test: ...)`. `tools/mkinit.py OBJ OUT [ENTS.plist]` adds an XML entitlements blob (special slot -5; default output byte-identical). QEMU `research/q0035-ent` (RAM disk `research/root-hfs-ent.img`, init with 3 test entitlements, highmem): `org.sweet.init: 3 entitlements (test: bool 1 string 1 array 1)` then init PID 1. MAC policies loaded: 0034 = 1, 0035 = 2 (QMP `mac_policy_list`). CI `38909807230` -> `xnu/out-0035`. Phone images: `shim/out/shim-boot-0035hr.img` (highmem, ro), `-0035hw.img` (highmem, +ufsrw=1 rootrw=1), `-0035r.img` (low mem fallback).
- **PHONE TEST ORDER (updated):** 0035hr -> if instant reset, 0035r -> then 0035hw.

- **HIGHMEM: XNU in the upper DDR bank, ~3.95 GiB (was 1.2 GiB).** Live FDT memory = <0x80000000 2G> + <0x1_00000000 0xfcc00000>; all fixed reserved-memory carve-outs are in the low bank (highest: ramdump_fb 0xaf000000, rmtfs ~0xfde01000), dynamic pools have alloc-ranges <= 0xffffffff, UFS node has no `iommus` (Linux DMAs anywhere). `tools/mkadt.py --highmem` sets /chosen dram-base 0x100000000 dram-size 0xfcc00000; `tools/mkpayload.py` now takes phys_base/mem_size from the ADT (default payloads byte-identical, verified); `tools/qemu-sweet.py` sizes -m from the payload (8G for highmem). Patch **0034** (`0034-sweet-ufs-dma-above-4g.patch`): UFS refuses DMA memory above 4G without UFSHCI CAP.64AS (bit 24), logs `DMA at 0x...`. CI `38905889883` success -> `xnu/out-0034`. **QEMU verified** (`research/q0034-hi`, ADT `research/q0034-hi.adt` --qemu --highmem, HFS RAM disk): phys_base 0x100000000, init PID 1 heartbeat, no panic; `max_mem` = `mem_size` = 0xfcc00000 read via QMP (`research/q0034-hi-mem`). Phone images: `shim/out/shim-boot-0034hr.img` (read-only) / `-0034hw.img` (+ufsrw=1 rootrw=1), ADT `shim/out/sweet-0034hi.adt` (asmb SIP + sweet-ufs + highmem). PHONE RISK: unknown runtime TZ/XPU protection in the upper bank would show as an instant reset; fall back to 0033r/w. Watchdog ruled out for the overnight reset: msm-watchdog bark is 20 s (qcom,bark-time 0x4e20) yet panic screens stay up for many minutes.

- **Offline research 2026-10-16 (user away, phone unavailable). Images rebuilt** `shim/out/shim-boot-0033r.img` / `-0033w.img` now also carry `wdt_test=no_user_checkin`. NEXT ON PHONE: boot 0033r (expect past in6_nigroup), then 0033w (first writes: rw root fixes HFS link-chain bits itself and gives /var for launchd sockets /var/run/syslog, /var/run/lockdown.sock).
- **launchd.plist** (`/System/Library/xpc/launchd.plist`, compiled; 532 daemons, 66 RunAtLoad/KeepAlive, list in scratchpad `early-daemons.txt`). `_PanicOnCrash` daemons: containermanagerd/usermanagerd (InternalOnly), lockdownd/remoted/trustd/remotepairingdeviced (AutomationOnly), **watchdogd unconditional** (KeepAlive SuccessfulExit=false). watchdogd needs IOKit `IOWatchdog` kext service; if absent it exits only when `kern.hv_vmm_present` (ADT `/defaults/vmm-present`, hvg_sysctl.c) or with boot-arg `wdt_test=no_user_checkin` ("detected testing boot-args to not run, exiting"; reads kern.bootargs). Using the boot-arg (vmm-present would change many daemons; keep as an option).
- **GUI path research (QuartzCore in the shared cache, `ipsw dyld str CACHE STR`, ~10 s/search):** CA::WindowServer has IOMFBServer/IOMFBDisplay (Apple DCP/IOMobileFramebuffer), AppleCLCDDisplay, AppleRGBOutDisplay, **VirtualServer/VirtualDisplay** and **MemorySurface**, EAGLServer. Renderers: CA::OGL::MetalContext, GLContext and a **CPU software rasterizer CA::OGL::SW** (samplers/blend modes; "image is too large for software renderer"). Env knobs: `CA_ENABLE_OGL`, `CA_DISPLAY_TYPE`, `CA_FORCE_LOCAL_SERVER` (249 CA_* vars). Hypothesis (unverified): backboardd's render server could run a VirtualServer/MemorySurface with the SW renderer and we copy the surface to the ABL framebuffer -> needs disassembly of CA::WindowServer server creation. Expected other GUI walls: IOSurface (closed-source kext; needs a reimplementation), IOMobileFramebuffer user client, IOHID touch events, AppleKeyStore/keybag (SEP) for lock state, MobileGestalt answers (AppleCLCD etc.).

- **0032r RESULT (boot 05:07:50 UTC, `research/boot0032r.log`, photo IMG_20261016_071200): SHARED CACHE MAPPED, LAUNCHD RUNS.** With SIP relaxed (ADT asmb) the `not in trust cache` lines are only warnings for every subcache (.31 ... .42.dyldlinkedit); no SIP rejection; libSystem loads; launchd configures networking (`skip attaching fsw to lo0 using legacy TX model`) -> kernel data abort far 0x28 in `SHA1Init` (symbolized as sha1_init) from `in6_nigroup` (IPv6 on lo0): g_crypto_funcs NULL. Kernel addresses are unslid: `~/swift/usr/bin/llvm-symbolizer --obj=KERNEL ADDR` works directly.
- **0032** BearSSL SHA-1 (`0032-sweet-bearssl-sha1.patch`), **0033** BearSSL SHA-384/512 (`0033-sweet-bearssl-sha384-sha512.patch`, BearSSL ctx stored in SHA512_CTX, static-asserted to fit; ubc_subr.c uses SHA-384 for code directories). `0020-stage-bearssl.sh` now also stages hash/sha1.c, hash/sha2big.c, codec/{dec,enc}{32,64}be.c. CI `38854909053` success (0032-only run `38854802073` superseded). Kernel `xnu/out-0033` (SHA1Init -> _br_sha1_init verified by disassembly; nm symbols have a leading underscore). Images (ADT sweet-0032): `shim/out/shim-boot-0033r.img` (read-only), `shim-boot-0033w.img` (+ufsrw=1 rootrw=1). Still NULL g_crypto_funcs users: des, chacha20poly1305, rsa, aesxts, rand, flow_divert.
- `research/check-patch-order.py` now skips patches touching CI-staged sweet_hfs sources (0031) instead of stopping.

- **0031r RESULT (boot 05:03:52 UTC 2026-10-16, `research/boot0031r.log`, photo IMG_20261016_070508): SHARED CACHE FOUND.** dyld now opens `dyld_shared_cache_arm64` (v2 image hard links), kernel refuses to map it: `shared_region: ... map(...'dyld_shared_cache_arm64'): not in trust cache` -> `vnode is not SIP-protected` (vm_unix.c: macOS arm64 path needs trust cache, else root-owned + SF_RESTRICTED unless CSR_ALLOW_UNRESTRICTED_FS) -> `dyld cache '(null)' not loaded: syscall to map cache into shared region failed` -> libSystem not loaded -> coredump to /cores fails error 30 (EROFS) -> panic initproc failed -> "MACH Reboot" (spins; screen kept). Lots of `hfs: set hardlink bit on vol=iOSRoot cnid=... linkid=...` spam (Linux-made hard links lack the link-chain bit; read-only mount cannot persist the fix). FIX: ADT `/chosen/asmb` with `lp-sip0`=0x6f (u64; incl. CSR_ALLOW_UNRESTRICTED_FS) and `lp-sip1`=1 (unauthenticated root), `tools/mkadt.py` -> `shim/out/sweet-0032.adt`. Images with kernel 0031: `shim/out/shim-boot-0032r.img` (read-only) and `shim-boot-0032w.img` (+ufsrw=1 rootrw=1).

- **2026-10-16 morning:** userdata now = **v2** image (`diff-v1-v2.simg` flashed 21:06:50 UTC 2026-10-15, OKAY, `research/flash-userdata-diff-v2.log`); future diffs use `ios16-root-20H392-v2.img` as OLD. Booted `shim-boot-0029k.img` (ignition_level=1) right after (`research/boot0029k-v2.log`); **no photo** (user asleep). Next morning the phone was in PixelOS recovery = some hardware reset (ABL then booted Android, which cannot use userdata). OBSERVATION: our kernel cannot reset the SoC itself (`PE_halt_restart` is never set; reboot/halt print "MACH Reboot"/"CPU halted" and spin), so the reset came from outside XNU: Qualcomm watchdog or a TZ/XPU violation. Unknown which; re-boot 0029k and watch/video until the reset. Do NOT tap factory reset/format data in recovery (would wipe the iOS image).
- **0030** (`xnu/patches/0030-sweet-ufs-writes.patch`, CI `38852655542`): UFS WRITE(10) + read-modify-write for partial 4 KiB blocks + SYNCHRONIZE CACHE (DKIOCSYNCHRONIZE), only with boot-arg `ufsrw=1`; `ufs_write_blocks` re-checks partition bounds before every write (only place data goes out).
- **0031** (`xnu/patches/0031-sweet-read-write-root.patch`, CI `38852837176`): boot-arg `rootrw=1` clears MNT_RDONLY before the root mount (no data volume on sweet: /private/var is on the root; image has no /etc/fstab); Apple HFS accepts a dirty non-journaled ROOT read-write on SWEET (logs "mounting dirty non-journaled root read-write"). Later: journaled HFS for crash safety. Kernel `xnu/out-0031` (CI `38852837176` success, 5m31s; 0030 run cancelled by the newer push). Boot images (phone ADT `sweet-0028.adt`, ramdisk byte-matched): `shim/out/shim-boot-0031r.img` = 0029k args (read-only, ignition_level=1) and `shim/out/shim-boot-0031w.img` = same + `ufsrw=1 rootrw=1`. PLAN: boot 0031r first and film until the reset (diagnose overnight reset), then 0031w (first ever writes to userdata; v2 image on the SSD is the restore source). `research/check-patch-order.py` cannot check 0031 (staged sweet_hfs files are not in its index); CI stage scripts run first, so CI is the check.

- **ignition_level=1 result** (boot 21:01:39 UTC, `research/boot0029k.log`, photo IMG_20261015_230308): preboot/cryptex stages skipped (need >= 2/3), `dylib_cache: finding shared cache on system volume: ignition level = 1, search root fd = 4, subpath = System/Library/Caches/com.apple.dyld/` -> not found -> `ignition boot failed: 19` -> no shared cache -> libSystem not loaded. FIX IN PROGRESS: image v2 = copy of the flashed image + `/System/Library/Caches/com.apple.dyld/` with HARD LINKS to the 44 cryptex cache files (no extra space; avoids symlink-following doubts), then `tools/sparsediff.py ios16-root-20H392.img ios16-root-20H392-v2.img diff.simg` and flash only the diff. Boot with `ignition_level=1` (shim-boot-0029k.img).
- **ignition_level=0 result** (boot 20:58:07 UTC, `research/boot0029j.log`, photo IMG_20261015_230037): all stages skipped as "ignition level insufficient" (hello/preboot/cryptex1 sniff >= 2, select os cryptex path/graft >= 3, **dyld_cache >= 1**), `ignition boot failed: 89`, "ignition partially disabled", then same `Library not loaded: /usr/lib/libSystem.B.dylib (no such file, no dyld cache)`. => dyld gets the shared cache directory from ignition's dyld_cache stage. Next: `ignition_level=1` (`shim/out/shim-boot-0029k.img`) to skip preboot/cryptex stages but run dyld_cache; its log "finding shared cache on %s ... subpath = %s" will show where it searches. If it searches rootfs /System/Library/Caches/com.apple.dyld, add a symlink there (image rebuild; consider a diff-only sparse flash tool to avoid rewriting 12 GB).
- **APPLE dyld/launchd RUNNING (libignition) with `unentitled_ios_sim_launch=1`** (boot 20:53:24 UTC, `research/boot0029i.log`, photo IMG_20261015_225617): kernel prints "Allowing spawn of iOS binary ... boot-arg set to true"; `shared_region: ... check_np ... vm_shared_region_start_address() failed` (no region yet, normal); dyld's built-in **libignition** (Darwin Ignition Sequence 1.0.0, libignition-51~1974; prints rd=ufsroot0, hardware target sweet, ignition level 0x5, platform 0x2, boot spec local, 7 stages): `hello from launchd.1` -> `preboot: mounting preboot` -> `failed to lookup preboot: 25` (ENOTTY: looks for a separate Preboot volume by role) -> ignition fails -> dyld `Library not loaded: /usr/lib/libSystem.B.dylib ... (no such file, no dyld cache)` -> launchd exit -> panic initproc failed. dyld boot-args found via strings: `ignition_level`, `ignition_force_dylib_root` (forced rootfs/livefs/cryptex fallback), `ignition_halt_after`, `ignition_live_app_graft`; dyld cache search paths include /System/Cryptexes/OS, /System/Volumes/Preboot/Cryptexes/OS/, /private/preboot/Cryptexes/OS/ (present in our image). Next try `ignition_level=0` (`shim/out/shim-boot-0029j.img`).
- **APPLE launchd EXECUTED FROM UFS (2026-10-15).** Flashed iOS image: `img2simg` -> `ios16-root-20H392.simg` (12.1 GB) then `fastboot -S 512M flash userdata ...simg` (24 chunks, 307 s, `research/flash-userdata-ios16.log`; a raw-image flash was killed by earlyoom at 2.6 GB RSS - always flash the sparse image). ABL fastboot hung on getvar after the flash; power+vol-down fixed it. Boot 0029u 20:49:04 UTC (`research/boot0029u-ios16.log`), photo IMG_20261015_225134: `hfs: mounted iOSRoot` -> load_init_program /sbin/launchd -> panic `unexpected SIGKILL of launchd (CS_KILLED) with reason -- namespace 9 code 0xe` = OS_REASON_EXEC / EXEC_EXIT_REASON_WRONG_PLATFORM: our kernel is XNU_TARGET_OS_OSX, iOS-platform binaries are "alien" and refused unless spawn attr platform set or DEVELOPMENT TUNABLE `unentitled_ios_sim_launch`. Next try: same kernel, cmdline + `unentitled_ios_sim_launch=1` (`shim/out/shim-boot-0029i.img`). LONGER TERM: macOS-config kernel marks iOS maps alien (vm_map_mark_alien) and differs from iOS in many policies; an iPhoneOS-config kernel build may eventually be needed.
- **iOS 16 ROOT IMAGE BUILT:** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392.img` (16 GiB case-sensitive HFS+, label iOSRoot, 12 GB used, fsck OK after `fsck.hfsplus -y` rewrote 32 non-ASCII localized WorkflowKit Shortcut names Linux decomposes differently). Built by `tools/mkiosroot.sh OS.dmg SYSTEMOS.dmg APPOS.dmg OUT.img [SIZE]` (needs sudo; apfs-fuse as root; OS dmg is UDIF -> link must end .dmg). Contents: iPhone X 20H392 OS root + SystemOS cryptex at /private/preboot/Cryptexes/OS (so /System/Cryptexes/OS -> cache, 44 files, dyld_v1 arm64) + AppOS at .../App. /sbin/launchd and /usr/lib/dyld root:wheel 0755. NEXT: (confirm) `fastboot flash userdata ios16-root-20H392.img` (auto-sparse), boot 0029u (rd=ufsroot0) -> Apple launchd attempt.
- **MILESTONE ON HARDWARE: BOOT FROM INTERNAL FLASH.** 0029 CI `38797924912` PASSED, `xnu/out-0029` SHA256 `a68bc847...2a37`. Image `shim/out/shim-boot-0029u.img` (payload-0029u = 0029 kernel + `shim/out/sweet-0028.adt` + `rd=ufsroot0`, NO RAM disk). Boots 20:01:34 and 20:12:37 UTC (`research/boot0029u*.log`), photo IMG_20261015_221403: `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB, read-only` -> `BSD root: ufsroot0, major 1, minor 0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `SWEET: root volume is not authenticated (error 25); continuing unsealed` -> `load_init_program ... /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> heartbeat (ran for minutes unattended). userdata currently holds the 8 MB `research/root-hfs.img`. NEXT: build a multi-GB HFS+ image with the iOS 16 (iPhone X 20H392) userland (OS rootfs + SystemOS cryptex contents incl. dyld shared cache at /System/Library/Caches/com.apple.dyld; preserve modes/owners/symlinks; decompress LZBITMAP via apfs-fuse), flash it to userdata (sparse, needs user OK), then try Apple's dyld/launchd. Driver is read-only (root mounts RDONLY), fine for first launchd attempts.
- **userdata FLASHED with the 8 MB HFS test volume** (user said "flash it", 2026-10-15 19:53:17 UTC, `research/flash-userdata-hfs-test.log`: `fastboot flash userdata research/root-hfs.img` OKAY; pre-checks: one sweet device, partition-size:userdata 0x1AC4BFB000, partition-type f2fs, image fsck OK, SHA256 3626ea69...). Android userdata is now destroyed (expected/approved). Boot 0028u at 19:53:20 (`research/boot0028u-hfs.log`), photo IMG_20261015_215541: `BSD root: ufsroot0` -> **`hfs: mounted SweetRoot on device b(1, 0)` from internal UFS** -> panic `rootvp not authenticated after mounting @bsd_init.c:931` (arm64 macOS-config requires FSIOC_KERNEL_ROOTAUTH sealed root for non-ramdisk roots). Patch **0029** (`dd1c284`): SWEET logs `SWEET: root volume is not authenticated (error N); continuing unsealed` instead of panicking (Apple configs keep the panic; pivot_root still requires auth). CI **`38797924912`** running. Next: download out-0029, phone image with sweet-0028.adt + rd=ufsroot0 (no RAM disk), boot -> expect init from UFS.
- **UFS ROOT DRIVER VERIFIED ON HARDWARE (read-only).** 0028 CI `38796139570` PASSED, `xnu/out-0028` SHA256 `8b981640...9da6`; QEMU HFS RAM-disk regression `research/q0028-hfs` still runs init. Phone boot 2026-10-15 19:50:24 UTC (`research/boot0028u.log`, image `shim/out/shim-boot-0028u.img`, phone ADT `shim/out/sweet-0028.adt` with /sweet-ufs, NO RAM disk, `rd=ufsroot0`), photos IMG_20261015_215151/215220: `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB, read-only` -> `BSD root: ufsroot0, major 1, minor 0` -> `hfs_ValidateHFSPlusVolumeHeader: unknown Volume Signature : f188` (Android-encrypted data, as expected) -> `cannot mount root, errno = 19`, kernel retries mountroot (no panic). Nothing written to flash. NEXT (destructive, needs user confirmation right before): `fastboot flash userdata research/root-hfs.img` (8 MB HFS with test init) then boot rd=ufsroot0 -> expect init from internal flash.
- **PATCH 0028 (`33aceac`): XNU read-only UFS root device**, CI **`38796139570`** running (next artifacts xnu/out-0028, research/bt29, run29.log). `bsd/dev/sweet_ufs.c`: reuses ABL's UFSHCI state (like the shim probe), takes over UTRL at a kmem_alloc_contig region (DMA layout: UTRL 0x0, UCD 0x1000, 1 MiB bounce 0x4000), verifies UTRLBA readback before any doorbell, IE=0 polled, one SCSI cmd at a time on LUN0 (TUR x3, READ(10) via bounce, PRDT 256 KiB chunks), flush_dcache64 by PA around each command (host not dma-coherent per DT), finds GPT partition by name (`ufsroot=` boot-arg, default `userdata`), exposes `/dev/ufsroot0`/`rufsroot0` (512-byte logical sectors, physical 4 KiB, DKIOC* ioctls), refuses writes (EROFS). IOKitBSDInit: `rd=ufsroot0` -> sweet_ufs_rootdev() (lazy init) else panic. ADT: `tools/mkadt.py` adds `/sweet-ufs` reg <0x1d84000 0x3000> for the PHONE only (not --qemu). Local compile OK, imports resolve. Sandbox research/bt28 (pre0028 originals). FIRST PHONE TEST PLAN (non-destructive): boot 0028 with phone ADT + `rd=ufsroot0` and NO RAM disk: expect `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB` + `BSD root: ufsroot0`, then root mount failure (userdata is still Android-encrypted) -> panic. That validates the driver before flashing an HFS image into userdata (needs explicit user confirmation at that time).
- **SUPERSEDES the 64 GiB iosroot GPT plan: user said "u can delete android" (2026-10-15).** Use the existing `userdata` partition (LUN0 sda34, 4K LBA 0x2B8C00, 0x1AC4B MiB ~107 GiB) directly as the iOS root: NO GPT changes. Keep bootloaders, recovery (OrangeFox), modem/persist/fsg/modemst untouched. Write the HFS image later with `fastboot flash userdata` (sparse, auto-split under the 768 MiB limit). Android will no longer boot normally (expected; reinstallable). Order: XNU UFS driver first, read-only against the current GPT; flash only once it can locate userdata. Nothing erased yet.
- **DECIDED (user, 2026-10-15): 64 GiB `iosroot` on LUN0 (sda), taken from userdata (wipes Android user data; Android/super kept).** Planned GPT (4K LBAs): userdata 0x2B8C00..0xD7D6FF (~43 GiB, keep type/unique GUIDs and attributes); iosroot 0xD7D700..0x1D7D6FF (0x1000000 blocks = 64 GiB, 1 MiB aligned); backup GPT area unchanged. Procedure: user backs up phone data -> boot OrangeFox recovery (adb) -> back up GPT (sgdisk --backup + raw dd of LBA 0-5 and last 6 blocks) to research/ -> sgdisk edit -> Format Data -> verify Android boots to setup. NOT EXECUTED YET.
- **INTERNAL UFS WORKS FROM THE SHIM (read-only), user authorized internal-UFS approach incl. flashing (2026-10-15, "i allow everything").** Shim probe `shim/ufs.c` (commit `12ed3ed` + filter): ufshc@1d84000 is UFSHCI 2.1 (ver 0x210, cap 0x1587031F, 32 slots), ABL leaves HCE=1, HCS=0x10F (device present, lists ready, UIC ready); probe takes over UTRL at its own buffer (verifies UTRLBA readback before any doorbell), TEST UNIT READY/READ CAPACITY/READ(10) all succeed. LUN0 = 0x1D7D800 x 4 KiB (~126.6 GB), valid GPT (64 entries at LBA 2). Photos IMG_20261015_212916/213325/213429. Big LUN0 partitions (start in 4K LBAs / MiB): super 0xCA00/0x2200 (8.5 GiB), logdump 0x22CA00/64, minidump 0x230A00/128, rawdump 0x238A00/128, recovery 0x240C00/128, cache 0x248C00/384 ext4, exaid 0x260C00/384, cust 0x278C00/1024 ext4, **userdata 0x2B8C00/0x1AC4B MiB (~107 GiB), fs unreadable = encrypted (metadata encryption)**. cache..cust contiguous = only 1.75 GiB (too small for iOS ~10+ GiB). Plan needing user consent: shrink userdata in GPT (wipes Android data) and add an `iosroot` partition at the end of LUN0. LUNs 1-5 not listed yet (sdb..sdf backed up in backup/lun).
- **fastboot limit measured (2026-10-15, read-only getvar):** `max-download-size: 805306368` (768 MiB); `max-fetch-size` unsupported; `is-userspace: no` (ABL fastboot). A `fastboot boot` image (shim+kernel+RAM disk) must be < 768 MiB, so the 2.5 GiB iOS shared cache cannot ride in the boot RAM disk even if XNU gets all RAM. Real userland needs storage access (UFS driver, or USB host) or a much smaller cache. Unlocking full RAM is still needed later (GUI).
- **iOS 16 USERLAND SOURCE (Claude, 2026-10-15).** Chose **iPhone X (iPhone10,3/10,6, D22/D221AP)** iOS **16.7.16 (20H392)** over iPhone 8: same A11 (no PAC -> plain arm64, runs on Kryo 470/ARMv8.2), last iOS for A11; X userland is home-button-less and tall-screen (1125x2436 vs sweet 1080x2400), better fit for later GUI. Note the X has its OWN SystemOS cryptex (different digest from iPhone 8's). IPSW URL in `research/ipsw-x/URL.txt` (+ BuildManifest). Images on the user's external SSD (NOT in git, do not format that disk: it holds the user's photos): `/run/media/dipa/android/ios-sweet-ipsw/iPhone10,3_16.7.16_20H392/` — `087-86593-047.dmg` = Cryptex1,SystemOS (2,743,074,816 B), `087-86698-044.dmg` = OS rootfs (4,730,814,044 B), both zip CRC-32 verified, plus Firmware/*.root_hash/.trustcache/.mtree. AppOS cryptex is 087-86715-047.dmg (10 MB, same as iPhone 8).
  - Images are raw APFS; files use LZBITMAP (decmpfs type 14). 7z cannot decode. Tools: `ipsw` 3.1.738 (AUR ipsw-bin, user-approved) needs apfs-fuse on Linux; **apfs-fuse** built in user space (system cmake broken: cmake 4.4.4 wants libjsoncpp.so.27, jsoncpp 1.9.6 installed = partial upgrade, NOT fixed) with pip cmake + `-DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_FLAGS="-include cstdint"`, installed to `~/.local/bin/apfs-fuse` (+apfs-dump-quick). Mount via a comma-free symlink (apfs-fuse splits options on ',' in `iPhone10,3`; exFAT has no symlinks -> put link elsewhere): `apfs-fuse LINK/087-86698-044.dmg MNT` -> `MNT/root/...`; unmount `fusermount3 -u MNT`.
  - Verified from headers: `dyld_shared_cache_arm64` magic `dyld_v1   arm64`; `/sbin/launchd`, `/usr/lib/dyld` = cputype 0x100000c subtype 0 (plain arm64). libSystem exists only inside the cache.
  - **BLOCKER for real userland via RAM disk:** shared cache = 3.10 GiB in 44 files (~2.5 GiB without the 592 MB `.symbols`), but the kernel manages only 1.20 GiB (0xb0000000..0xfd000000). Options: (A) give XNU the phone's full ~6 GB (banks 0x80000000+2G and 0x100000000+0xfcc00000, carve-out holes need pmap support) AND check fastboot max-download-size for a multi-GB boot image; (B) storage driver (Qualcomm UFS) to read a root from flash (no flashing allowed: would need a file/partition strategy); (C) run against individual dylibs extracted from the cache (uncertain).
- **MILESTONE ON HARDWARE: HFS+ ROOT FILESYSTEM -> PID 1.** Boot 2026-10-15 18:22:12 UTC (`research/boot0027b.log`, image `shim/out/shim-boot-0027b.img`), photo `IMG_20261015_202334.jpg`: `BSD root: md0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> repeated `SWEET init: still alive`, no panic. Kernel 0027 (built-in Apple OSS HFS + BearSSL MD5), init with SP alignment fix. NEXT: real iOS 16 userland on the HFS image (dyld, libSystem/dyld shared cache, launchd). Known gaps: entitlements (none granted), SHA-1/SHA-384/512 providers, no storage driver (RAM disk only), root mounted read-only.
- **PHONE HFS ROOT (0027) + SIGBUS ROOT-CAUSED.** Phone boot 2026-10-15 17:49:06 UTC (`research/boot0027.log`, photo `IMG_20261015_200031.jpg`): `hfs: mounted SweetRoot on device b(1, 0)` (HFS works on hardware), init printed its first line, then `pid 1 exited -- exit reason namespace 2 subcode 0xa` = SIGNAL/SIGBUS -> `initproc failed to start` panic. Diagnostic boot 18:08:13 UTC (`research/boot0027d.log`, image `shim/out/shim-boot-0027d.img`, diag init `research/diag-init` from scratch diag-init.S with [a][b][c] markers, `cs_debug=1`; photo `IMG_20261015_201547.jpg`): output `PID [a][b]` then SIGBUS -> fault at first `strb w21,[sp]`; no code-signing messages. Cause: kernel enters a static binary with sp at argc, not necessarily 16-aligned (depends on arg/apple string lengths, differs mockfs vs HFS); EL0 SP alignment check -> EXC_ARM_SP_ALIGN -> SIGBUS (sleh handle_sp_align). QEMU does not enforce SP alignment. NOT a kernel bug: real binaries start in dyld which aligns. Fix `1a8fc15`: sweet-init aligns sp at entry. Rebuilt `research/root-hfs.img`, QEMU `research/q0027-hfs2` OK. Phone image `shim/out/shim-boot-0027b.img` SHA256 `098ba46c...c5c` (payload-0027b, ramdisk match check-0027b) ready, awaiting FASTBOOT. Lesson: Assembly `;` is a comment in Apple arm64 asm (use .macro, not ;-joined #define).
- **HFS ROOT WORKS (QEMU).** 0027 CI `38779441895` PASSED, `xnu/out-0027` SHA256 `a8643886...5f6a`. QEMU `research/q0027-hfs` (RAM disk = `research/root-hfs.img`, rd=md0): `BSD root: md0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` + heartbeat, no panic. Phone image `shim/out/shim-boot-0027.img` (payload-0027 = 0027 kernel + sweet-0021.adt + root-hfs.img + rd=md0, ramdisk byte-match check-0027) ready; awaiting FASTBOOT for phone test.
- **HFS ROOT WORK (Claude), patches 0026-0027.**
  - 0026 (`f0e990c` + link fix `64c96f4`): Apple OSS **hfs-627.100.6** (commit `31d5ec238dfab485e78a9a30b8b92d13e8914f03`, paired with xnu-8796.141.3 in macos-135 release.json) staged by `xnu/patches/0026-stage-hfs.sh` into `bsd/sweet_hfs` (core + hfs_encodings; AppleKeyStore include/key prototypes guarded by CONFIG_PROTECT; SDK TargetConditionals copied). New config option `sweet_hfs` (MASTER + MASTER.arm64.sweet); 40 `optional sweet_hfs` files; Makefile.template foreach adds `_CFLAGS_ADD = -include sweet_hfs_compat.h -I...` (MUST come after kernel -D flags; compat undefs BSD/XNU_KERNEL_PRIVATE and the CONFIG_* HFS tests so kext-config.h decides: macOS profile, no content protection). `sweet_hfs_iokit.c` replaces hfs_iokit.cpp/hfs_encodings_kext.cpp: `sweet_hfs_register()` called in bsd_init after vfsinit (encodings init, vfs_fsadd VFS_TBLCANMOUNTROOT, zones, sysctls); is_ejectable 0, iterate_media none, serial KERN_NOT_SUPPORTED, OSKextGetCurrentLoadTag -> kOSKextInvalidLoadTag (renamed via compat macro). hfs_encodings' own `hfs_allocated` renamed per object (separate kexts on Apple; first CI `38777325964` failed on that duplicate at link). mockfs now validates Mach-O magic (its TODO) so non-Mach-O roots fall through to HFS (new fs entries come AFTER mockfs in vfsconf). CI `38778133720` PASSED, `xnu/out-0026` SHA256 `0b49170c...701a`, prints `SWEET HFS: hfs-627.100.6 registered`.
  - HFS+ image: `research/root-hfs.img` (8 MB, mkfs.hfsplus from AUR hfsprogs installed with user approval; loop-mounted with sudo; /sbin/launchd = research/sweet-init, /dev; fsck.hfsplus OK). QEMU `research/q0026-hfs`: `BSD root: md0` then data abort in MD5Init from hfs_getvoluuid (mount computes volume UUID).
  - 0027 (`14bf2b7`): 0020 stager also copies BearSSL hash/md5.c + codec/dec32le.c/enc32le.c; `corecrypto_md5.c` SWEET branch converts MD5_CTX <-> br_md5_context around br_md5_* calls; wrappers sweet_md5.c/sweet_dec32le.c/sweet_enc32le.c. Host test 40/40 match md5sum. CI **`38779441895`** running.
  - Local tooling: `tools/xnu-cc.py` has `XNU_CC_POST` (flags after logged ones). Sandbox `research/bt28/xnu` = 0025 CI tree + 0026/0027 edits; originals `research/pre0026`, `research/pre0027`. HFS local objects `research/hfs-objs`. Checker entries updated to bt28.
  - SHA-1 / SHA-384/512 still have no provider.
- **MILESTONE ON HARDWARE: USERSPACE PID 1 RUNS ON THE PHONE.** Boot 2026-10-15 17:16:00 UTC (`research/boot0025.log`: send OKAY0.410s, boot OKAY0.135s), image `shim/out/shim-boot-0025.img` SHA256 `9dbfa0b1...89db0`. Photo `IMG_20261015_191733.jpg`: `BSD root: md0` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> repeated `SWEET init: still alive` (5 s heartbeat), no panic. Kernel 0025 + mockfs RAM disk + built-in no-entitlements AMFI. No flashing performed.
- **NEXT (toward real iOS userland):** real root filesystem with real binaries. Options: (a) build Apple OSS `hfs` (macOS 13.5 tag `hfs-627.100.6`) into SWEET like libpthread, then an HFS RAM disk image; (b) iOS 16 dyld + libSystem/dyld shared cache from the IPSW (needs APFS or repacking onto HFS). Expected hurdles: entitlements (sweet_amfi grants none), SHA-1/MD5/SHA-384/512 providers (BearSSL), missing kexts/daemons. Current init is a static test program, not launchd.
- **MILESTONE: USERSPACE RUNS (QEMU).** 0025 CI `38774788048` PASSED, `xnu/out-0025` SHA256 `5496069b...4877`. QEMU `research/q0025-rd` (150 s, no panic): `BSD root: md0` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> `SWEET init: still alive` every 5 s. Exec, ad-hoc SHA-256 code signature, syscalls, devfs /dev/console, select timeouts all work. Phone image prepared: `shim/out/shim-boot-0025.img` 16,515,072 bytes SHA256 `9dbfa0b15140c0bd733a16c4f727f6a7df44a8741f98d8e266d5f2fa4f689db0` (payload-0025 = 0025 kernel + sweet-0021.adt + research/sweet-init + rd=md0; ramdisk byte-match check-0025). Waiting for user to put phone in FASTBOOT.
- **0024 CI `38773277811` PASSED**, `xnu/out-0024` SHA256 `a0ba964b...4348`. QEMU `research/q0024-rd` and **PHONE (boot 2026-10-15 17:05:55 UTC, `research/boot0024.log`, image `shim/out/shim-boot-0024.img` SHA256 `cf3dac86...6964`, 16,510,976 bytes, payload `shim/out/payload-0024.bin` = 0024 kernel + `shim/out/sweet-0021.adt` + RAM disk `research/sweet-init` + rd=md0; ramdisk byte-match `check-0024`)** agree: `Added memory device md0`, `BSD root: md0`, `load_init_program: attempting to load /sbin/launchd`, then data abort in accelerate_entitlement_queries (PC 0x...77d2458, FAR 0x1a0) = NULL AMFI interface. Photo `IMG_20261015_190715.jpg`. RAM disk root is physically verified.
- **0025 (`2518c79`)**: new `bsd/kern/sweet_amfi.c` registers a built-in AMFI interface at EARLY_BOOT/MIDDLE: no entitlements (adjustContextWithoutMonitor succeeds without creating a context, queries KERN_DENIED, copies NULL/KERN_NOT_FOUND, get_xml/transmuted false); WithMonitor KERN_NOT_SUPPORTED; OSEntitlements_query and query_context_to_object panic explicitly (CoreEntitlements closed; no kernel caller); TrustCache version 0 (0015 keys on trust_cache_rt==NULL, img4 absent -> still unavailable); CoreEntitlements table zero (PMAP_CS only). Compiles locally; checker updated (bt27 entries). CI **`38774788048`** running. Next artifacts `xnu/out-0025`, `research/bt29`, `research/run29.log`. Real iOS binaries will need real entitlements later (no OSS CoreEntitlements exists).
- **0021-0024 RAM-disk-root iteration (Claude), QEMU only so far, no new phone boot since 0020.** Each kernel tested with `tools/mkpayload.py KERNEL research/q0021.adt OUT --ramdisk research/sweet-init --cmdline "debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=md0"` then `tools/qemu-sweet.py OUT DIR --secs 150 --kernel KERNEL --fail-on-panic` (PATH needs ~/swift/usr/bin for llvm-nm). Fresh ADTs: `research/q0021.adt` (QEMU), `shim/out/sweet-0021.adt` (phone).
  - 0021 CI `38769532000` PASSED, `xnu/out-0021` SHA256 `2b7500a1...962e`, `research/bt25`/`run25.log`. QEMU `research/q0021-rd`: md0 root, then assert `iomediaClass` in IOService::publishHiddenMedia.
  - 0022 (`20ece9c`, publishHiddenMedia without IOMedia class) CI `38770666158` PASSED, `xnu/out-0022` SHA256 `a4d0e787...30c5`, `research/bt26`/`run26.log`. QEMU `research/q0022-rd`: data abort in SHA256_Init (NULL g_crypto_funcs) from vm_kernel_addrhash_internal.
  - 0023 (`c8089d1`, libkern SHA256_Init/Update/Final use built-in ccsha256_ltc_di + ccdigest_init/update on SWEET; also serves code-signing SHA-256; SHA-1/MD5/SHA-384/512 still have NO provider - BearSSL from 0020 could supply them later) CI `38771876423` PASSED, `xnu/out-0023` SHA256 `d763fed7...1003`, `research/bt27`/`run27.log`. QEMU `research/q0023-rd`: **mockfs mounted md0, `load_init_program: attempting to load /sbin/launchd`**, then panic `mockfs_fsnode_vnode failed to create fictitious pages ... rvalue = 5` (mockfs.c:351).
  - 0024 (`3293c80`): mockfs used memdev mi_base (4K page number of a VIRTUAL kernel address for IOKit RAMDisk, truncated to 32 bits) << PAGE_SHIFT as a physical address. Now zero-copy pager mapping only when mi_phys (with 4K units); virtual md uses pagein/blockmap/strategy -> memdev bcopy. memdev's own mdPhys path assumes 4K ppnums (unsafe on 16K arm64), so do NOT switch the RAMDisk to physical. CI **`38773277811`** running. Next artifacts `xnu/out-0024`, `research/bt28`, `research/run28.log`.
  - Sandboxes: bt25/bt26/bt27 contain the next patch's edited files; pristine copies in `research/pre0022`..`pre0024`.
- **PATCH 0021 (Claude): RAM disk root via mockfs -> first userspace program.** Commits `9c37771` (initial; CI `38768500280` FAILED: mockfs_fsnode.c kfree_type(mockfs_fsnode_t) typed-alloc static assert; local xnu-cc stubs `__builtin_xnu_types_compatible` so it can't catch this) and `193772f` (fix), CI **`38769532000`** running: https://github.com/dipa-studio/ios-sweet/actions/runs/38769532000. Next artifacts: `xnu/out-0021`, `research/bt25`, `research/run25.log`.
  - Kernel: `config/MASTER.arm64.sweet` FILESYS_BASE += `mockfs` (XNU's built-in FS: root device is itself a Mach-O, served as /sbin/launchd, plus /dev for devfs). Upstream mockfs bit-rot fixed: kalloc_type/kfree_type used the POINTER typedef mockfs_fsnode_t (nodes were 8 bytes) -> `struct mockfs_fsnode`. `IOService::setRootMedia` asserted IOBlockStorageDriver class exists (IOStorageFamily absent): SWEET-only, a missing class means root=NULL (same as IOSetImageBoot); Apple path keeps assert. All 21 patches apply (`research/check-patch-order.py`); 5 TUs compile locally with -DMOCKFS (`research/mockfs-objs`), imports resolve vs 0020 kernel. Sandbox `research/bt24/xnu` now holds 0021 versions of those 3 files; pristine 0020 copies in `research/pre0021`.
  - Tools: `tools/mkpayload.py --ramdisk IMAGE` appends IMAGE as an extra payload segment right after the kernel, moves kernel_end past it (shim unchanged: ADT+boot_args follow it, image stays below topOfKernelData), and adds ADT `/chosen/memory-map` `RAMDisk`=<phys,size>. Boot with `rd=md0`. Without --ramdisk output is byte-identical to existing 0020 QEMU and phone payloads (verified). `tools/sweet-init.S` + `tools/mkinit.py`: PIC static init (open /dev/console, print PID, heartbeat every 5 s via select, never exits) wrapped into a static arm64 Mach-O (__PAGEZERO, __TEXT@0x100000000, LC_UNIXTHREAD, ad-hoc SHA-256 CodeDirectory v0x20400, 4K pages). Build: `~/swift/usr/bin/clang -target arm64-apple-ios16.0 -c tools/sweet-init.S -o X.o && tools/mkinit.py X.o research/sweet-init` (ld64.lld cannot link static iOS). Signature not verified by a real codesign; the kernel will tell.
  - QEMU with 0020 kernel + RAM disk (`research/q0020-rd.bin`, rd=md0, 150 s `research/q0020-rd150`): `Added memory device md0`, **`BSD root: md0, major 1, minor 0`** (plumbing works), then the setRootMedia assert (now fixed in 0021). NOTE: QEMU needs >60 s to reach IOFindBSDRoot (60 s run showed nothing after stf0; likely RTC/inittodr wait), so use --secs 150.
  - NEXT: download 0021, QEMU 150 s with ramdisk; expect mockfs mount then init exec -> `*** SWEET userspace: init running as PID 1 ***`. Then phone boot with same payload (phone ADT shim/out/sweet-0020.adt pattern + --ramdisk + rd=md0).
- **0020 PHONE RESULT (user transcription of screen, 2026-10-15): KERNEL INIT COMPLETE, WAITING FOR ROOT.** After Skywalk self-tests PASSED, kminit, ifnet_attach lo0/gif0/stf0, screen prints `BSD`, then `Waiting on <dict><key>IOProviderClass</key><string>IOMedia</string><key>Content</key><string>Apple_HFS</string></dict>` and `Failed to write boot-picker-bringup-reason to NVRAM.` No panic. This is IOFindBSDRoot waiting for a root device (none exists); NVRAM warning is expected (no NVRAM driver). QEMU `cpu_idle` snapshot is presumably the same wait (not GDB-confirmed; milestone GDB run was cancelled by user since phone answered it). Draft `research/check-milestones20.gdb` (hbreaks inittodr/vfs_mountroot/IOFindBSDRoot/bsd_utaskbootstrap) left uncommitted/ignored.
- **NEXT MILESTONE: root filesystem -> launchd.** Plan: (1) RAM disk: shim places an image in RAM, ADT /chosen/memory-map `RAMDisk` entry, boot-arg `rd=md0` (XNU md driver). (2) HFS is a separate kext on Apple; build Apple OSS `hfs` (tag paired with macOS 13.5 in distribution-macOS macos-135 release.json) into SWEET like libpthread 0019. APFS is closed. (3) Minimal HFS image with iOS 16 launchd (later: dyld/shared cache; AMFI/code-signing absent will be a later hurdle). User's end goal is full iOS GUI.
- **0020 (AES) VERIFIED + PHONE BOOTED (Claude took over after Codex usage limit).** Actions `38765422261` (`ab9e23f`) PASSED; kernel `xnu/out-0020/kernel.development.sweet` checksum OK; buildtree `research/bt24`, log `research/run24.log`. Actual-kernel AES checks PASS (`research/check-aes20.gdb` / `.log`, 12 extra CBC cases match OpenSSL). 45s QEMU `research/q0020`: no panic, zero unknown glyphs, past old TCP/AES panic -> Skywalk self-tests PASSED -> bsd_autoconf kminit -> ifnet_attach lo0/gif0/stf0; final snapshot PC in `cpu_idle` (idle or waiting; NOT yet diagnosed, could be root-device wait). Image `shim/out/shim-boot-0020.img` 16,461,824 bytes SHA256 `775200cb02d95fc750981516b79d91dcdc96184bbe67a38f9d57c59b4a391828`, ramdisk byte-matches `payload-0020.bin` (`check-0020`). **Phone temporarily booted 2026-10-15 16:10:00 UTC**: one FASTBOOT product sweet, send OKAY0.407s, boot OKAY0.134s, total0.549s, exit0 (`research/boot0020.log`). Awaiting user photo; do not reboot the phone before it. NEXT: read photo; diagnose what QEMU waits on after stf0 (GDB backtrace of threads / longer run). Codex's STOP request below is complete.
- User requests STOP after completing the current0020 AES iteration (Actions/QEMU/phone), then leave a precise committed handoff for another AI. User says FASTBOOT ready again after0019 photo. Do not start a new blocker fix after this iteration.
- Goal: iOS16-generation XNU on Redmi Note10Pro sweet/SM7150. Always commit, use gh/Actions for kernel builds, keep this handoff current. Temporary fastboot boot only; preserve Android/backups. No userland/root filesystem boot yet.
- **Patch0020 update:** initial `e71098d` / Actions `38765012466` superseded by scalar-only compile flags. Added -mgeneral-regs-only to all six provider/BearSSL TUs and corecrypto_aes.c; object disassembly now confirms no SIMD. Updated implementation `ab9e23f`, Actions `38765422261` queued/running: https://github.com/dipa-studio/ios-sweet/actions/runs/38765422261. Do not launch another run. portable BearSSL AES CBC and legacy one-block ECB wired directly into SWEET corecrypto_aes.c. Genuine bitslice implementation, no CPU AES/SIMD requirement, heap or fake global crypto table. Source fetched by `0020-stage-bearssl.sh` from official BearSSL git at immutable `7bea48e5e850ab4cafbe68d3765cdaba13a86d6f`; MIT license retained, downloaded source stays out of git. Kernel limits include adapter only. All128/192/256-bit keys, CBC encrypt/decrypt, copied contexts, in-place/out-of-place; zero block count and size overflow handled, invalid keys clear context. Seven TUs compile to arm64 objects (`research/aes-objs`), imports resolve, all20 patches apply and sources match (`research/patch0020-check.log`). Sandbox `research/bt23/xnu`, originals `research/pre0020`. NEXT: Actions then actual-kernel NIST/random CBC/ECB checks and >=45s QEMU before another phone boot. Next artifacts out-0020 / bt24 / run24.log. 0020 updated CI pending. Local sources/checks match the scalar-only patch.
- **Latest built kernel0019**, implementation `256d3f0`, patches0001-0019. Actions `38763072907` PASSED (4m5s): https://github.com/dipa-studio/ios-sweet/actions/runs/38763072907. Kernel `xnu/out-0019/kernel.development.sweet`, SHA256 `a27df7568f03fb541cf0e8024c0a594fa178a85054fcf9eba29158cbd4c5ecc0`; checksum verified. Log/source `research/run23.log` / `research/bt23` (no nested .git). Seven pthread source/build/header files and staged adaptations byte-match local compile inputs.
- **0019 hardware photo received** `IMG_20261015_175306.jpg`: pthread registration visible, passes mbinit and DLIL checksum/scheduling, same AES fault as QEMU: PC`0xfffffe00079174e0` (`aes_encrypt_key128`), LR`0xfffffe000767c3a4` (`tcp_init`), FAR0x78, x8=0. Disassembly proves NULL g_crypto_funcs->ccaes_cbc_encrypt. Photo processed; no more0019 observation pending. General crypto table remains absent, other hash/mode operations may still fault after0020. DO NOT bypass TCP or install fake crypto. XNU already contains SHA256/HMAC implementations; AES source there is a dispatch wrapper. Full future provider interface libkern/libkern/crypto/register_crypto.h. Apple/corecrypto default README describes evaluation-only licensing, so no external corecrypto was fetched or staged; BearSSL selected for this portable AES integration.
- **0019 pthread FIXED in QEMU and observed beyond its init on phone**: 45s QEMU `research/q0019`, zero unknown glyphs, then AES panic. Actual-kernel API checks PASS `research/check-pthread19.gdb` / `.log`, guest `research/q0019-api`: function/callback table identity, actual provider pthread_init returns, locks/global hash/threadcall/typed zones initialized, thread_selfid via syscall shim + buffer bounds, process hash init/delete via shims restores NULL. Monitor quit prints expected remote-disconnect after PASS. All fixture guests stopped.
- **0019 provider**: genuine Apple libpthread-514.100.2 commit `a6c70ca0e544347a0377babf748f831577ec24f9`, exact paired release with xnu8796.141.3 in distribution-macOS/macos-135/release.json (`research/macos-135-release.json`). 0019 shell stage runs before patches (workflow copies *.sh); three SWEET wrapper TUs use kext BSD header view, vm_fault_external, renamed provider-side pthread_kern/current_uthread; register real function table at EARLY_BOOT SECOND, real pthread_init later. Stager applies bounded address casts, zero user addresses, proper panic format. SWEET opaque ksyn storage enlarged48->56 for trailing kwe_uth, checked with provider static assertion. Local pre-CI TargetConditionals fixture was syntax-only; artifact bt23 carries actual SDK header and CI is authoritative.
- **Phone0019 temporarily booted** 2026-10-15 15:51:36 UTC: exactly one FASTBOOT/product sweet verified; send OKAY0.406s, boot OKAY0.134s, total0.546s, exit0 (`research/boot0019.log`). Image `shim/out/shim-boot-0019.img`, 16,457,728 bytes, SHA256 `19429a57e486b856880df9e27327ed488e0139345311fdb0350974e72103a9a1`. Phone ADT/payload `shim/out/sweet-0019.adt` / `payload-0019.bin` timer19, unpacked ramdisk byte-match (`check-0019`). EntryPA0xb146b488, kernelendPA0xb2000000, boot_argsPA0xb2004000/top0xb2008000. Last user FASTBOOT+USB reply preceded this boot; do not assume phone is still in FASTBOOT.
- **CPU0018 physically verified** by `IMG_20261015_173951 (2).jpg`: boot CPU0 registered, real SGI1 verified, initialization complete -> BSD/MAC/mbinit -> old pthread-table panic. SweetCPU uses legacy IOCPU, ml_processor_register/processor_start/initCPU, real SGI1 clears SIGPdisabled before max CPUs completion; no forced flags/skipped waits. CPU APIs and two-CPU rejection passed (`research/check-cpu18.gdb`, `q0018-api`, `q0018-smp`). Single core; SMP/suspend unsupported. CURRENT SWEET has NO USE_APPLEARMSMP.
- QEMU next run: generate fresh `tools/mkadt.py research/q0020.adt --qemu` (timer27), mkpayload with `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`, then `tools/qemu-sweet.py PAYLOAD OUT --secs 45 --kernel KERNEL --fail-on-panic`. 12s can miss later panics because IORTC waits30s. Runner snapshot only: panic exit2, blank/incomplete exit3; absence of panic does not mean complete boot. Qualcomm XPU/ABL/panel and phone SMC PSCI require hardware checks.
- Local checker `tools/xnu-cc.py research/run23.log research/bt23 FILTER --per-file`, XNU_CC_OBJDIR for objects. For new BearSSL TUs add XNU_CC_EXTRA with -I bt23/xnu/libkern/crypto/sweet_bearssl/{inc,src}. Patch checker `research/check-patch-order.py` uses temporary upstream index; source fixtures/artifacts ignored under research. GDB mask registers to unsigned64, use function-entry manual-call return traps, discard manipulated guests. No QEMU guest intentionally left running.

## Session log and earlier handoffs (superseded by the active summary above)

### Prior 0019 transition notes (superseded)

- Goal: iOS 16 generation XNU on sweet. Always commit completed work, use gh/Actions for kernel builds, keep this handoff current. Temporary fastboot boot only; preserve Android/backups.
- **0019 build PASSED** Actions `38763072907` (4m5s), implementation `256d3f0`. Kernel `xnu/out-0019/kernel.development.sweet`, SHA256 `a27df7568f03fb541cf0e8024c0a594fa178a85054fcf9eba29158cbd4c5ecc0`; checksum verified. Log/source `research/run23.log` / `research/bt23`; all seven patched files and staged provider adaptations match local compile inputs. Prefer bt23 as the next baseline.
- **0019 pthread FIXED in QEMU**: 45s run `research/q0019` registers provider, passes mbinit, DLIL SUM16 checks and DLIL thread scheduling. Actual-kernel GDB checks `research/check-pthread19.gdb` / `.log` PASS: function/callback table identity, real _pthread_init returns, locks/global hash/cleanup threadcall/typed zones non-NULL, thread_selfid via actual syscall shim with output bounds, process hash init/delete through actual shims restores NULL. Guest stopped after tests; no fixture left running. GDB monitor quit prints expected remote disconnect after PASS.
- **Current next blocker:** QEMU0019 panic data abort FAR0x78 at `aes_encrypt_key128` PC`0xfffffe00079174e0`, called by `tcp_init` LR`0xfffffe000767c3a4`. Disassembly confirms `g_crypto_funcs == NULL`, loading ccaes_cbc_encrypt at+0x78. General crypto registration is still absent; DO NOT bypass TCP or supply fake crypto. Next integrate a genuine compatible crypto implementation/provider (AES first needed here, other digest/mode APIs also used). XNU contains SHA256/HMAC but no AES implementation; its corecrypto_aes.c is a dispatch wrapper. Full crypto table is in libkern/libkern/crypto/register_crypto.h.
- **0019 phone image prepared and verified**, user reports FASTBOOT+USB again; exactly one device/product sweet verified. `shim/out/shim-boot-0019.img`, 16,457,728 bytes, SHA256 `19429a57e486b856880df9e27327ed488e0139345311fdb0350974e72103a9a1`; unpacked ramdisk matches phone payload (`shim/out/check-0019`, `payload-0019.bin`, `sweet-0019.adt`, timer19). EntryPA0xb146b488; kernelendPA0xb2000000; boot_argsPA0xb2004000/top0xb2008000. Usual debug cmdline cpus=1/-noprogress. **Temporarily booted 2026-10-15 15:51:36 UTC**: send OKAY0.406s, boot OKAY0.134s, total0.546s, exit0 (`research/boot0019.log`). User asked for photo after45s. Await the photo; DO NOT reboot again before observation. Bootloader acceptance only; no0019 physical progress observed yet.
- **Hardware photo confirms 0018 progress** (`IMG_20261015_173951 (2).jpg`): real phone prints `SWEET CPU: boot CPU 0 registered, SGI1 verified, initialization complete`, enters BSD/MAC, reaches `mbinit: done`, then the same missing-pthread-function-table panic as QEMU at pthread_shims.c:318. CPU completion/interrupt delivery is now physically observed. The photo was received; no further phone boot performed yet.
- **Patch0019 committed/pushed `256d3f0`; Actions `38763072907` queued/running:** https://github.com/dipa-studio/ios-sweet/actions/runs/38763072907. Do not launch a duplicate. genuine Apple OSS libpthread-514.100.2 provider (immutable commit `a6c70ca0e544347a0377babf748f831577ec24f9`), paired with xnu-8796.141.3 by Apple's `distribution-macOS/macos-135/release.json` (`research/macos-135-release.json`). `0019-stage-libpthread.sh` fetches/stages it before patches; workflow now copies shell scripts too. SWEET-only wrappers compile all three real kernel sources, rename provider-side symbols, use kext header view and vm_fault_external, register the real function table at EARLY_BOOT SECOND. Existing pthread_init then runs the actual provider initialization. No pthread wait/syscall is bypassed. Source staging includes bounded explicit address casts/zero user addresses and panic-format fixes. SWEET kernel opaque ksyn storage enlarged from48 to56 bytes to contain this provider's trailing kwe_uth, with a provider size assertion. Local compile of three provider TUs plus pthread_shims/kern_fork passed; imports resolve and provider exports do not collide with existing kernel symbols. All19 patches apply and changed sources match (`research/patch0019-check.log`). Source sandbox `research/bt22/xnu`, originals `research/pre0019`, objects `research/pthread-objs`. Local TargetConditionals fixture only has target macros for syntax; CI stages the real macOS SDK header and is authoritative. Next Actions artifacts: out-0019 / bt23 / run23.log; run QEMU >=45 seconds. 0019 CI is pending; no 0019 QEMU run yet.
- **Latest kernel implementation `e7d9550`, patches0001-0018; CI `38760004398` PASSED (3m56s)**: https://github.com/dipa-studio/ios-sweet/actions/runs/38760004398. No build is pending. Kernel `xnu/out-0018/kernel.development.sweet`, SHA256 `b3c8d59acc88f93a2c836eb2527a05ed4fbaac7c580a2ea8c3b795137f4aadf1`; checksum verified. Source/log `research/bt22` / `research/run22.log` (baseline for patch0019; no nested .git). New driver/config sources match CI exactly.
- **CPU wait FIXED in QEMU**: SweetCPU uses legacy IOCPU, validates single boot CPU, ml_processor_register -> processor_start -> initCPU real SGI1 -> scheduler/IOKit completion -> ml_set_max_cpus. It does NOT force a flag or skip a wait. CPU APIs passed: Running CPU0, processor_array[0] association, SGI signalling enabled, name, unsupported secondary-start error (`research/check-cpu18.gdb` / `.log`, `research/q0018-api`). Single-core only; SMP and suspend unsupported. Two-CPU topology fails explicitly (`research/q0018-smp`).
- **Next blocker reproduced in 45s QEMU** (`research/q0018-long`, zero unknown glyphs): BSD initialization reaches MAC framework, network mcache and `mbinit: done`, then **`pthread kernel extension not loaded (function table is NULL). @pthread_shims.c:318`**. Do not bypass pthread_init: find/integrate the matching open-source libpthread kernel implementation and register its real function table. A 12s run `research/q0018` looked panic-free before the 30s IORTC wait elapsed; use >=45s or GDB checkpoints for the next iteration. No userland/root filesystem boot yet.
- **Phone 0018 TEMPORARILY BOOTED** 2026-10-15 **15:31:15 UTC**: exactly one FASTBOOT device verified product sweet; send OKAY0.400s, boot OKAY0.134s, total0.539s, exit0. Local log `research/boot0018.log`. This confirms bootloader acceptance only. User was asked for a photo; await it, DO NOT reboot the phone again before their observation. No flashing performed.
- Current hardware image `shim/out/shim-boot-0018.img`, **16,437,248 bytes**, SHA256 **`b7a23595d143a76c72c9fe2cfcc5d77a8f16987b5af1a2703bbffdfa6922908c`**. Phone ADT/payload `shim/out/sweet-0018.adt` / `shim/out/payload-0018.bin` (timer19), unpacked ramdisk exactly matches payload (`shim/out/check-0018`). EntryPA0xb146b488; kernelendPA0xb1ffc000; boot_argsPA0xb2000000/top0xb2004000. Command line `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`.
- QEMU payload/ADT `research/q0018.bin` / `research/q0018.adt` (timer27). Run `python3 tools/qemu-sweet.py research/q0018.bin research/NEW-OUT --secs 45 --kernel xnu/out-0018/kernel.development.sweet --fail-on-panic`; fresh ADT seed for a new payload. Output fb.png/fb.txt/regs.txt/qemu.log/result.json. Visible panic exit2; blank/incomplete decode exit3; no_panic_observed is snapshot-only, not successful boot. -noprogress prevents the graphical indicator corrupting console text. Qualcomm XPU/bootloader/panel and SMC PSCI still need physical validation.
- Patches0014-0017 fixed PRNG registration/direct SHA256, explicit unavailable trust-cache service with rejected loads/no matches, built-in SweetPlatformExpert, and timer PPI from ADT (phone19/default19, QEMU27). All their checks/artifacts are preserved in the history below. CURRENT SWEET has NO USE_APPLEARMSMP; do not assume gCPUIC/gAIC/gPMGR AppleARMSMP globals exist.
- Local single-file checker: tools/xnu-cc.py research/run22.log research/bt22 FILTER --per-file, output via XNU_CC_OBJDIR. Patch checker `research/check-patch-order.py` applies all18 via temporary index, matches sandbox sources. Sandbox for0018 `research/bt21/xnu`, originals `research/pre0018`, objects `research/cpu-objs`. First compiler issues were missing machine/atomic.h and nonexistent getNameSymbol; fixed and both TUs compiled successfully before CI. Fixtures/artifacts under research are local-only/ignored.
- GDB: mask int(register)&((1<<64)-1) for unsigned kernel pointers; use function-entry manual-call return traps, discard manipulated guests. No QEMU fixture is intentionally left running.

### Earlier active handoff snapshot (superseded)


- **0018 milestone:** Actions `38760004398` PASSED (3m56s), checksums passed, new CPU/build files byte-match CI tree. Kernel `xnu/out-0018/kernel.development.sweet`, SHA256 `b3c8d59acc88f93a2c836eb2527a05ed4fbaac7c580a2ea8c3b795137f4aadf1`; log/tree `research/run22.log` / `research/bt22`. QEMU `research/q0018` 12s: boot CPU registered, SGI1 verified, CPU initialization complete, **BSD initialization entered** (copyright, MAC framework, buffer headers), no panic/zero unknown glyphs. Direct CPU API checks PASS (`research/check-cpu18.gdb`, `.log`, `research/q0018-api`): CPU0 Running, processor matches processor_array[0], real SGI enabled, CPU name correct, secondary-start returns KERN_NOT_SUPPORTED. Two-CPU ADT correctly panics before registration (`research/q0018-smp`). Longer 45s run `research/q0018-long` still running; next BSD wait/fault not yet identified.
- **Prepared 0018 phone image:** `shim/out/shim-boot-0018.img`, 16,437,248 bytes, SHA256 `b7a23595d143a76c72c9fe2cfcc5d77a8f16987b5af1a2703bbffdfa6922908c`. Phone ADT/payload `shim/out/sweet-0018.adt` / `shim/out/payload-0018.bin`, usual debug args with cpus=1 and -noprogress. Unpacked ramdisk byte-compared (`shim/out/check-0018`). Entry PA remains 0xb146b488; kernel end PA 0xb1ffc000, boot_args 0xb2000000/top0xb2004000. User reports FASTBOOT+USB ready; read-only check found exactly one product sweet. NEXT: temporary fastboot boot of this verified image, record send/boot results, then await hardware photo without rebooting again.
- Patch 0018 committed/pushed **`e7d9550`**; Actions **`38760004398`** queued/running: https://github.com/dipa-studio/ios-sweet/actions/runs/38760004398. Do not launch a duplicate run.
- Active continuation: patch **0018** implemented in `iokit/Kernel/arm/SweetCPU.cpp` + arm64 source list + exact qcom,kryo470 personality. Keeps legacy IOCPU, accepts ONLY the single boot CPU, fills ml_processor_info from parsed topology with CPU object as cpu_id, calls ml_processor_register and processor_start. initCPU sends SGI1 via ICC_SGI1R_EL1 and waits (1-second deadline) for real cpu_signal_handler to clear SIGPdisabled. Only after successful startup calls ml_cpu_init_completed/cpusRunning and publishes completion/max CPUs. Secondary startup/suspend are explicitly unsupported. Local C++ compile passed for both TUs (`research/cpu-objs`), all imports resolve, object contains dsb ishst / ICC_SGI1R / isb; all18 patches apply in order and match sources. Sandbox `research/bt21/xnu`, originals `research/pre0018`; next CI artifacts should use `xnu/out-0018`, `research/bt22`, `research/run22.log`. User has the phone available; first run QEMU, then prepare/temporarily boot useful hardware progress.
- Goal: iOS 16 generation XNU on Redmi Note 10 Pro / sweet. User wants persistent progress, commits, kernel builds via `gh` Actions, and this handoff kept current across agent switches. Temporary `fastboot boot` only; preserve Android and backups.
- Latest kernel implementation: **`aa3f991`**, patches **0001-0017**. All four new Actions builds PASSED: 0014 `38748543058` (4m0s), 0015 `38749549779` (4m3s), 0016 `38750733996` (4m3s), 0017 **`38751507437` (4m7s)**. Latest: https://github.com/dipa-studio/ios-sweet/actions/runs/38751507437. No build is pending.
- **Current blocker: CPU initialization has no SWEET CPU driver.** QEMU registers SweetPlatformExpert, then kernel_bootstrap_thread waits in **kperf_init_early -> ml_wait_max_cpus**. Confirmed via actual-kernel GDB call stack (`research/locate-cpu-wait2.log` / `.symbols`) and normal-run `max_cpus_initialized == 2` (MAX_CPUS_WAIT). Do not force the flag or remove the wait. Next implement real CPU registration and completion using XNU's CPU/processor interfaces. CURRENT SWEET uses legacy IOCPU (`USE_APPLEARMSMP` is absent); enabling AppleARMSMP is a separate architectural change requiring GIC/PMGR services. No userland/root filesystem boot yet.
- Fixed this session: PC=0 unregistered PRNG callback (0014, built-in HMAC-SHA256 provider + direct entropy/write_random hashing); absent Image4/AMFI trust-cache service (0015, unavailable runtime, loads rejected and queries no-match); missing platform driver (0016, SweetPlatformExpert exact personality); incorrect QEMU timer IRQ (0017, validated ADT PPI property, phone default19/QEMU27).
- **Latest kernel** `xnu/out-0017/kernel.development.sweet`, SHA256 `055a80190ab998b4df9203f1102072dcc78faad1779a537a514e522b682b582f`. Buildtree/log **`research/bt21` / `research/run21.log`**; all nine changed C/C++/header/config files byte-match local checked sources. Checksums passed. Entry PA `0xb146b488`, kernel end PA `0xb1ff4000`. Preferred baseline for patch 0018: `research/bt21/xnu` (no nested .git).
- **QEMU verified**: `research/q0017-noprogress` ran **30 seconds**, no visible panic, **zero unknown glyphs**, IRQ exceptions returned normally (4 IRQs, tickless idle). It still waits for CPU completion, so this is NOT a completed boot. Earlier 15s run `research/q0017` captured 122 IRQs, timer value27, GICR_ISENABLER0 `0x08000002`, and CPU WAIT; graphical progress overlay corrupted 13 glyphs. Add **`-noprogress`** to keep the console readable. New runner classifies incomplete/blank decoding explicitly (exit3 with --fail-on-panic), visible panic exits2. Snapshot-only; use regs/GDB to diagnose stalls.
- Current QEMU payload/ADT: **`research/q0017-noprogress.bin` / `research/q0017.adt`**. Run: `python3 tools/qemu-sweet.py research/q0017-noprogress.bin research/NEW-OUT --secs 30 --kernel xnu/out-0017/kernel.development.sweet --fail-on-panic`. Generate fresh seed with mkadt for a new payload. QEMU virt models generic ARM execution, not Qualcomm XPU/bootloader/panel or the phone's SMC PSCI conduit.
- **Prepared phone image**: **`shim/out/shim-boot-0017.img`**, 16,416,768 bytes, SHA256 `51ff7fe30b4a6668c3452ffe1da922c5ac30cb8de60625c2a652587ecbd0ec92`. Phone ADT/payload `shim/out/sweet-0017.adt` / `shim/out/payload-0017.bin` (timer19). Unpacked ramdisk exactly matches payload (`shim/out/check-0017`). Command line **`debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`**. NOT sent to phone this session: known CPU-driver wait should be addressed in QEMU first. Last actual phone boot remains 0013; user's latest photo `IMG_20261015_160033.jpg` confirmed the old PRNG PC=0 panic.
- Direct QEMU/GDB API checks: PRNG 600-byte chunking, buffer bounds, changing output, zero-length reads/writes, user reseed, contended refresh, generator1 init/output PASS again on latest0017 (`research/check-prng17.gdb` / `.log`, guest `research/q0017-api`). Trust-cache unavailable-service/argument/output cases PASS on0015 (`research/check-trustcache.gdb` / `.log`). Platform registration + target/product normal/truncated/zero/null/bounds PASS on0016 (`research/check-platform.gdb`, `research/check-platform3.log`). Different platform ID correctly retains IOPanicPlatform fallback (`research/q0016-negative`). Timer PPI32 and size2 correctly panic (`research/q0017-badppi`, `research/q0017-badsize`); omitted property selects19 (`research/q0017-default`). These are API/bring-up checks, not crypto certification or SMP scheduling validation.
- Local checker **`research/check-patch-order.py`** verifies all17 patches and changed source equality using a temporary upstream git index. Fixtures/logs/artifacts under research are local-only and ignored. For GDB unsigned kernel pointers, mask `int(register_value) & ((1<<64)-1)`; x30/x29 may be rendered signed. Stop at a function entry for manual-call return traps, and discard each manipulated guest after API tests. All fixture QEMU guests have been stopped.


- User wants persistent progress toward iOS 16, commits for completed changes, builds through `gh` / GitHub Actions.
- Keep this file current at every milestone so another agent can resume immediately, including when usage limits interrupt a session.
- Patch 0017 committed/pushed `aa3f991`, Actions `38751507437` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38751507437. Next artifacts: xnu/out-0017, research/bt21, research/run21.log. Do not duplicate.
- Patch 0016 kernel downloaded/checksum verified: SHA256 `d06336c54baa06e0df6561a8bd7df98a9b9f7502c9381c62d1a44c045cd1ce46`, `xnu/out-0016/kernel.development.sweet`; buildtree/log `research/bt20` / `research/run20.log`. QEMU `research/q0016` (10s) prints platform expert registered, zero unknown glyphs, no panic observed BUT stalls (timer mapping still wrong until 0017). Direct actual-kernel GDB tests passed for registered instance and target/product names, including maxLength=1/0 and NULL, sentinels intact (`research/check-platform.gdb`, `research/check-platform3.log`, `research/q0016-api3`). First two fixture attempts used premature/wrong return breakpoints; discarded, corrected fixture uses start-return observation then a function-entry return trap. No phone boot yet.
- Patch 0016 CI `38750733996` PASSED (4m3s); artifacts not yet downloaded/booted. Patch 0017 prepared to fix QEMU timer fidelity BEFORE interpreting future no-panic/stall runs: actual `qemu-system-aarch64 -M virt,gic-version=3,dumpdtb=research/qemu-virt.dtb ...` timer property has virtual PPI 11 => INTID 27, while phone uses INTID 19. Kernel formerly hardcoded 19. New optional /arm-io/gic virtual-timer-intid property selects the PPI (validate exact u32 and 16..31); missing property retains phone default 19. One RO-late global drives GIC enable and sleh_irq dispatch. tools/mkadt.py emits phone19/QEMU27. Both C TUs compile (`research/timer-objs`), ADT serialize/parse checks confirm values/addresses, all 17 patches apply and match. Sandbox `research/bt19/xnu`, originals `research/pre0017`; initial local sleh compile failed due read-only exported header not updated, fixed export and BOTH recompiled successfully. CI exports normally.
- Architecture correction for next agent: CURRENT SWEET board_config does NOT define USE_APPLEARMSMP; it compiles the legacy IOCPU path, not cpu_boot_thread/IOPMGR AppleARMSMP. Existing roadmap mentions AppleARMSMP as a future approach. Do not look for gCPUIC/gAIC/gPMGR globals in the current kernel: they are absent. Determine the actual CPU-init wait after platform registration before choosing the next driver architecture.
- Patch 0016 committed/pushed as `0dcdf5c`; Actions `38750733996` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38750733996. Next artifacts: `xnu/out-0016`, `research/bt20`, `research/run20.log`.
- Patch 0016 implemented: new `iokit/Kernel/arm/SweetPlatformExpert.cpp`, arm64 source list, built-in personality in KernelConfigTables.cpp guarded by ARM64_BOARD_CONFIG_SWEET. Matches only xiaomi,sweet at score 10000, keeps IOPanicPlatform fallback for other hardware. Uses IODTPlatformExpert base initialization/power domain and createNubs CPU logical-ID annotation; overrides top-level publishing because base requires nonexistent Apple NVRAM /options. Publishes real CPU/top-level nodes, provides bounded target/product names, and registers the platform service. GIC/PMGR and arm-io child-bus drivers remain separate work. Both C++ TUs compile (`research/platform-objs`), all imports resolve against 0015/own objects, all 16 patches apply and sources match. Sandbox `research/bt19/xnu`; originals `research/pre0016`. NEXT: full Actions/QEMU; inspect CPU boot waits after the platform registers, do not equate absence of panic with successful boot.
- Patch 0015 CI `38749549779` PASSED (4m3s), checksum verified. Kernel `xnu/out-0015/kernel.development.sweet`, SHA256 `ca1b424a596c7058550ad1659080a333e7643270f019656401d80bf2b876645f`; buildtree/log `research/bt19` / `research/run19.log`. QEMU `research/q0015` (10s, zero unknown glyphs) passes trust-cache handling and machine lockdown, then panics `Unable to find driver for this platform: "xiaomi,sweet" @IOPlatformExpert.cpp:2319` (IOPanicPlatform fallback). Next concrete work: add a built-in SWEET IODTPlatformExpert personality/class; keep the fallback for mismatched platforms. No phone boot yet.
- Direct trust-cache API checks PASSED in the actual 0015 kernel under QEMU/GDB (`research/check-trustcache.gdb`, `research/check-trustcache.log`, `research/q0015-api`): runtime pointers NULL, hash/UUID queries return NOT_FOUND, typed/untyped/legacy loads return NOT_SUPPORTED, capabilities outputs zero and bounds preserved, invalid-argument cases still reject. Second PRNG check also verifies contended refresh returns immediately (`research/check-prng2.log`, `research/q0014-api2`).
- Patch 0015 committed/pushed `8f851d4`, Actions run `38749549779` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38749549779. Do not duplicate.
- Direct PRNG API checks passed in the REAL 0014 kernel under QEMU/GDB, stopped before trust-cache init (`research/check-prng.gdb`, log `research/check-prng.log`, guest `research/q0014-api`). Invoked read_random for 600 bytes (chunking and buffer sentinel intact), repeated output differed, zero-length read/write succeeded, write_random(64-byte input) succeeded, secondary generator 1 initialized and generated distinct output. QEMU log has no exceptions during these checks; guest was discarded after the tests. This tests API behavior, not a cryptographic certification or SMP scheduling.
- Patch 0015 implemented in `bsd/kern/kern_trustcache.c`: SWEET with missing Image4/AMFI marks both runtime pointers NULL and logs service unavailability. Existing static loader handles NULL. Public load APIs return KERN_NOT_SUPPORTED; hash/UUID queries return KERN_NOT_FOUND; capabilities outputs are zero with KERN_NOT_SUPPORTED. Invalid-input checks remain, and Apple paths/available-provider initialization retain existing behavior. No trust is granted. Local arm64 compile passed (`research/trustcache-objs`), all 15 patches apply and sources match. Sandbox `research/bt18/xnu`, baseline `research/pre0015`. Next: Actions/QEMU and direct unavailable-service API checks using GDB.
- Patch 0014 CI `38748543058` PASSED (4m0s), artifact checksum passed. Kernel `xnu/out-0014/kernel.development.sweet`, SHA256 `741de20c851755d333759d7e668346f3edb4f325efac4cc7c142d80d1f5ff75c`; buildtree/log `research/bt18` / `research/run18.log`. QEMU run `research/q0014` (10s, zero unknown glyphs) prints `SWEET PRNG: HMAC-SHA256 registered`, passes commpage initialization, loads vnguard policy, THEN panics `image4 interface not available @kern_trustcache.c:253`. PC=0 fault FIXED IN QEMU. No new phone boot performed.
- Next work: SWEET currently has neither AppleImage4 nor AMFI. `trust_cache_runtime_init` unconditionally requires both; unlike BCM2837, SWEET enters this startup path. Investigate an explicitly unavailable trust-cache runtime with rejected loads/no query matches while providers are absent; preserve all Apple-platform checks. Merely skipping the startup call would leave later AMFI/IMG4 dereferences unsafe. Existing load_static_trust_cache already handles trust_cache_rt == NULL.
- QEMU runner now supports `--kernel MATCHING_KERNEL --fail-on-panic`: runtime font extraction from the payload produces exact `fb.txt`, plus `result.json`; a visible panic returns 2. Baseline 0013 re-run `research/q0013-text` detects the same NULL callback panic with zero unknown glyphs. Synthetic glyph roundtrip (including literal `?`) and invalid-VA rejection passed. Screen rows remain circular, not a full log; `no_panic_observed` does not prove successful boot. README has the invocation.
- Patch 0014 committed/pushed as `be61f99`; Actions run `38748543058` is running: https://github.com/dipa-studio/ios-sweet/actions/runs/38748543058. Do not start a duplicate build.
- 2026-10-15 active: hardware photo `IMG_20261015_160033.jpg` confirms the same PC=0 instruction-fetch abort as QEMU (LR `0xfffffe0007443fe4` = read_random). Independently reproduced with kernel 0013 in `research/q0013` (8-second run); prior allocator fix works. Latest tooling commit reviewed: `8d66d2d`.
- Patch 0014 implemented: registers a built-in HMAC-SHA256 DRBG provider at EARLY_BOOT/FIRST, before commpage creation. A shared mutex serializes output/reseed across CPUs (correctness first; no per-CPU scaling yet), initgen validates CPU identities, refresh uses try-lock and the existing entropy filter/health tests. SWEET entropy accumulation and write_random now use the built-in SHA256 directly; no incomplete g_crypto_funcs table is registered. The existing bootloader-seed requirement remains enforced.
- Local validation: both PRNG translation units compile to arm64 objects in `research/prng-objs`; no SHA256 wrapper imports remain. All 14 patches apply in CI order and resulting PRNG sources match local inputs. Sandbox `research/bt17/xnu`, originals `research/pre0014`, checker `research/check-patch-order.py`. NEXT: Actions kernel build, download to `xnu/out-0014`, run the QEMU payload before requesting another phone boot. Baseline QEMU ADT/payload are `research/q0013.adt` / `research/q0013.bin`.
- 2026-10-15 08:15 QEMU EMULATION WORKS (`tools/qemu-sweet.py`, see "QEMU emulation" below). Patch 0013 VERIFIED in QEMU: boot passes kmem_crypto_init and ulock_initialize. NEXT BLOCKER (reproduced in QEMU, expected on hardware too): `pmap_create_commpages -> random() -> RandomULong -> read_random -> prng_funcs.refresh == NULL` (instruction fetch abort at pc 0, lr read_random+0x34). Nobody calls `register_and_init_prng` (closed corecrypto kext does it on Apple). Fix = patch 0014: SWEET-registered cckprng_funcs provider (osfmk/prng/prng_random.c); note random_cpu_init also panics while !prng_ready. The 07:26 hardware boot of 0013 will most likely show this same panic.
- Previous hardware boot: patch 0013 (`a3a46e2`) CI `38686345689` PASSED (3m44s), image `shim/out/shim-boot-0013.img` was temporarily booted on 2026-10-15 at 05:26 UTC: send OKAY (0.407s), boot OKAY (0.134s), total 0.546s. Superseded by the hardware/QEMU PC=0 observation and patch 0014 work above.
- Latest kernel implementation commit: `8f851d4`. Latest successful kernel CI: `38749549779` (patch 0015), https://github.com/dipa-studio/ios-sweet/actions/runs/38749549779.
- CURRENT image: `shim/out/shim-boot-0013.img`, 16,412,672 bytes, SHA256 `110d1c46aee4b60253db24b6535e9781c4cf0fd25ca2a70e9016cf81378cea25`. Kernel `xnu/out-0013/kernel.development.sweet`, SHA256 `f0b1d375995316c550ce7014ff234d8271e9b9ac2857795ceff41b76ba2cd740`, plain arm64. CI log confirms 0013 applied; checksums passed. Entry PA `0xb146b488`, kernel end PA `0xb1ff4000`.
- Current log/buildtree: `research/run17.log`, `research/bt17` (extracted, no nested .git; preferred baseline for patch 0014). Payload/ADT: `shim/out/payload-0013.bin`, `shim/out/sweet-0013.adt` (includes /defaults). Unpacked ramdisk byte-compared with payload in `shim/out/check-0013`.
- Patch-0012 original image: `shim/out/shim-boot-0012.img`, 16,412,672 bytes, SHA256 `cf4b8ec4a65a51888d71c17d09cd0831d6b761b90e2531fdb8e575c32f4fd24a`. Kernel `xnu/out-0012/kernel.development.sweet`, SHA256 `69b78f49f6459cc63a0af44e7cf73c1779ef72130ef72b12ae86c88183ffc742`; checksums passed and sweet_early_relocate symbol present. Entry PA remains `0xb146b488`, kernel end PA `0xb1ff4000`.
- Patch-0012 log/tree: `research/run16.log`, `research/bt16` (extracted, no nested .git; preferred baseline for next patch). CI log confirms 0012 applied. Payload `shim/out/payload-0012.bin`, ADT `shim/out/sweet-0012.adt`; packed ramdisk byte-compared with payload in `shim/out/check-0012`.
- Active payload command line: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam`.
- Latest observed photo: `/home/dipa/Downloads/IMG_20261015_071346.jpg` (local only). Stages 9 (kernel framebuffer VA), 10 (TTBR0 off/TLB flush), 11 (physmap table pointers) and 12 (calling pmap_bootstrap) all visible. Persistent diagnostics are VERIFIED ON HARDWARE.
- pmap.c:1987 is the assert after SecureDTLookupEntry(NULL, "/defaults", &entry). The pmap-max-asids property itself is optional; an empty /defaults uses XNU's MAX_ASIDS. Do not bypass the assertion or guess an ASID limit.
- Previous payload-only fix image: `shim/out/shim-boot-0012-defaults.img`, SHA256 `3ff61a268853c6ea7cbf284833f1346a1d791980ca366b6e1a215a86e040512b` (16,412,672 bytes). Same kernel/CI as 0012; ADT 2516 bytes (`shim/out/sweet-0012-defaults.adt`), root /defaults present with no ASID override. Payload `shim/out/payload-0012-defaults.bin`; unpacked ramdisk exactly matches payload (`shim/out/check-0012-defaults`). This boot reached the allocator crypto NULL-pointer fault below.
- Latest hardware photo: `/home/dipa/Downloads/IMG_20261015_071608.jpg` (local only). Normal serial framebuffer console works. VM bootstrap/zone initialization, logging, scheduler, IPC, KDP and ulock_initialize print before the kmem_crypto_init data abort. gPanicBase warnings are expected because PLATFORM_PANIC_LOG_DISABLED is configured, and are not the faulting call.
- Faulting instruction: `ldr x0, [x8, #0x150]` in crypto_random_kmem_ctx_size; x8 = NULL g_crypto_funcs. Source: libkern/crypto/corecrypto_rand.c and osfmk/vm/vm_kern.c:2448. rand.h explicitly permits NON-cryptographic kmem RNGs, but requires no locking in generation and context size <=256. Do not substitute read_random here: the global PRNG provider is also unregistered and kmem generation must remain lock-free. early_random may seed contexts during single-CPU bootstrap; it uses the built-in HMAC-SHA256 DRBG with the host-generated ADT seed.
- Patch 0013 keeps the replacement entirely private to vm_kern.c: SplitMix64 state is 8 bytes per CPU/sizeclass, initialized using early_random. Uniform selection uses rejection sampling to avoid modulo bias. Other platforms retain the original corecrypto calls; SWEET's generic crypto APIs/registration remain untouched. Reference: https://prng.di.unimi.it/splitmix64.c (Sebastiano Vigna, public domain).
- Validation: vm_kern.c compiles to arm64 (`research/kmem-rng-objs`, using `research/run16.log` + `research/bt16`). Undefined symbols include early_random and NO crypto_random_* references. All 13 patches apply in CI order and match the checked source. Original saved as `research/vm_kern.pre0013.c`.
- RNG host checks: extracted actual new helper in `research/kmem-rng-check.c`; 16,384 outputs match the author's downloaded reference (`research/splitmix64-reference.c`), 147,456 bounded outputs satisfy their limits (including 1 and UINT64_MAX), and a forced rejection advances correctly. Full kernel crypto services and the registered kernel PRNG provider remain future work; this patch only supplies the allocator RNG contract.
- Patch-0011 artifacts: kernel `xnu/out-0011/kernel.development.sweet`, log `research/run15.log`, extracted buildtree `research/bt15` (no nested .git). CI log confirms patch 0011 applied; artifact checksums passed. Kernel is plain arm64, entry VA `0xfffffe000746b488` -> PA `0xb146b488`, kernel end PA still `0xb1ff4000`.
- Patch-0011 image: 16,412,672 bytes, SHA256 `29ad5cbfc752473de4af2c471a24a8b34f92da4bff5afec65c614b90cd3ad53a`. Kernel SHA256 `8ac3a956894b09f7bd0d890de8c5de38c65513287feb1e1bcd12db8ca772ee5c`. Payload/ADT in `shim/out/payload-0011.bin`, `shim/out/sweet-0011.adt`. Header unpacked/checked in `shim/out/check-0011`.
- First patch-0011 attempt timed out waiting for FASTBOOT; superseded by the successful send/boot recorded above. Do not repeat the boot before the user reports the current screen.
- Patch-0011 photo: `/home/dipa/Downloads/IMG_20261015_070218.jpg` (local only). Visible stages 1-8 and old red shim text; entry PA B146B488, boot args PA B1FF8000 / top B1FFC000. No evidence yet locating execution after stage 8.
- Patch-0012 sandbox: `research/bt15/xnu` (NO nested .git). Proposed permanent debug VA: VM_MIN_KERNEL_ADDRESS + ARM_TT_L2_SIZE, in the reserved gap below gVirtBase and above low globals; map the same PA framebuffer as Normal-NC in the final TTBR1 before arm_vm_physmap_init changes phystokv(). Keep the early panic sink until normal kprintf startup.
- Patch 0012 validation: all 4 changed C translation units compiled to arm64 objects in `research/post-ttbr0-objs`; internal header export added to osfmk/arm64/Makefile and recreated locally in EXPORT_HDRS for pe_serial.c. All 12 patches apply in CI order and match all 6 edited files. Baselines are saved under `research/pre0012/`.
- Actual mapping-helper host model (`research/early-map-check.c`, barrier stubbed only for host compilation) confirms: VA `0xfffffe0002000000`, L1 index 2016, L2 index 1; descriptor `0x006000009c000605` = framebuffer PA, Normal-NC, outer-shareable, EL1 RW, PXN+UXN. All other L2 entries preserved. The gap is excluded by ARM_LARGE_MEMORY's pmap_virtual_region(0).
- Next boot command line MUST add `-enable_kprintf_spam`: DEVELOPMENT disables kprintf_output by default even when DB_KPRT is set (`pexpert/arm/pe_kprintf.c`). Planned command line: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam`.

### Patch 0012 screen legend (after original stages 1-8)
- 9: kernel framebuffer VA live; 10: TTBR0 off / TLB flushed; 11: physmap pointers rebound.
- 12: calling pmap_bootstrap; 13: pmap_bootstrap returned; 14: early I/O page tables ready; 15: arm_vm_init returned.
- 16: calling serial_init; 17: fbcon config read / mapping; 18: fbcon mapping returned; 19: serial_init returned; 20: kprintf startup complete.
- Normal serial initialization clears the screen, so earlier stages may disappear before 19. If serial exists, early console disables after 20; otherwise early panic output stays enabled.
- Local source sandbox: `research/bt13/xnu` (git baseline `623b060`, patches 0001-0008 already in baseline; uncommitted export edits correspond to patch 0009). Preserve those edits when producing patch 0010.
- Previous compile log/tree: `research/run13.log`, `research/bt13`; previous kernel: `xnu/out/kernel.development.sweet`. New successful log/tree: `research/run14.log`, `research/bt14`; new kernel: `xnu/out-0010/kernel.development.sweet`.
- Current device access: patch-0012 image was temporarily started from FASTBOOT; no adb connection is expected. Never flash partitions for bring-up; use `fastboot boot` with the shim image.
- Patch `0010` lives in `xnu/patches/0010-sweet-early-framebuffer-debug.patch`. Its exact compiled sources are under `research/bt13/xnu`; generated objects are in `research/early-objs`.
- Local checks passed: all 5 changed/new translation units compiled to arm64 Mach-O objects; new console only imports `_doprnt` and `iso_font` (both exist in the previous kernel). All 10 patches applied to a temporary upstream git index in CI order, and all 7 resulting changed source files matched the local compile inputs.
- Reproduce changed-file compilation: `XNU_CC_OBJDIR="$PWD/research/early-objs" python3 tools/xnu-cc.py research/run13.log research/bt13 arm_init.c arm_vm_init.c kern/debug.c arm64/start.s osfmk/arm64/sweet_early.c --per-file` (create the output directory first). The helper now accepts explicit new source paths absent from the old artifact's Makefiles and rejects empty selections.
- Device command result: `adb reboot bootloader`, then `timeout 30s fastboot boot shim/out/shim-boot-0010.img`: send OKAY (16028 KB), boot OKAY, total 0.541s. This confirms bootloader acceptance only, not XNU progress.
- The successful boot above was on 2026-10-14. On 2026-10-15, `timeout 45s fastboot boot ...` timed out waiting for a device; no image was sent. Boot image SHA256 rechecked and unchanged. No new build is needed to repeat the trial.
- Earlier retry: `timeout 90s fastboot boot shim/out/shim-boot-0010.img` timed out (exit 124). This is superseded by the successful 2026-10-15 repeat boot recorded above; do not repeat it until the user reports the screen.
- User observation confirms MMU-on C entry, platform expert, CPU topology/bootstrap, startup bootstrap and cpu_init all complete. Failure is within arm_vm_physmap_init (non-XNU_MONITOR branch), before stage 8 / TTBR0 teardown. Old red shim text remains behind the early console; this is expected because only written rows are cleared.
- New edit/compile sandbox is `research/bt14/xnu` (extracted artifact, NO nested .git; `git diff` there would act on the parent project). Use a saved baseline file / generated unified diff, or explicitly initialize a local baseline before editing. `research/bt13/xnu` does have its own baseline git repo.
- Exact user-reported panic: `arm_vm_init.c:1606 Assertion failed: (temp_ptov_table[ptov_index - 1].va + temp_ptov_table[ptov_index - 1].len) <= physmap_end`.
- Root cause: MacOSX build sets `ARM_LARGE_MEMORY=1`; `XNU_MONITOR` is off. Block alignment in arm_vm_physmap_slide can add gaps, but the non-PPL large-memory physmap_end omitted the padding already present in the small-memory branch. Patch 0011 reserves PTOV_TABLE_SIZE*ARM_TT_TWIG_SIZE (8*32MB) in both the aperture bound and its L1 allocation; monitor/PPL builds retain zero padding. The assertion is preserved.
- Validation: `arm_vm_init.c` compiled to an arm64 object using `research/run14.log` + `research/bt14` (object in `research/physmap-objs`). All 11 patches apply in CI order and produce exactly that source. Host harness `research/physmap-check.c` extracts the real XNU slide function with page-table-write stubs: all 65,536 page-aligned slides within 1GB checked against the current kernel memory layout; old bound fails 65,504 cases, padded bound fails zero; worst overrun 0x1ffc000 bytes. Baseline source saved as `research/arm_vm_init.pre0011.c`.
- CI: https://github.com/dipa-studio/ios-sweet/actions/runs/38638702083 (success; artifacts and full log downloaded).
- New image: `shim/out/shim-boot-0010.img` (16,412,672 bytes, SHA256 `ed2c270e0081bad5ff517be415f9bfe8805463aea7866732203fa97ac737e64e`). Previous image preserved as `shim/out/shim-boot-pre0010.img`.
- New kernel SHA256: `3ee05270cc291c49589a101678f904b1b69cb2f2575e05398bce8a4e052f409a`. Artifact checksums passed; arm64 (not arm64e), early-console symbols present. Payload entry VA `0xfffffe000746a488` -> PA `0xb146a488`; kernel end PA `0xb1ff4000`. Command line remains `debug=0xc serial=3 cpus=1 keepsyms=1`.

### Patch 0010 screen legend
- Bottom-left white 64x32 tile: assembly entered `start_first_cpu`, before page tables/MMU.
- Text `SWEET EARLY 1`: entered `arm_init` with MMU on; 2: platform expert done; 3: CPU topology done; 4: CPU bootstrap done; 5: startup bootstrap done; 6: CPU init done; 7: entering `arm_vm_init`; 8: leaving bootstrap TTBR0.
- `SWEET EARLY PANIC:` prints a copy of panic arguments before normal panic handling needs per-CPU/thread state.
- In patches 0010/0011 the console disabled before TTBR0 invalidation; patch 0012 replaces that with a persistent kernel VA alias and diagnostics through normal serial/kprintf startup (see its legend above).
- Screen contents require a physical observation from the user: adb cannot capture a framebuffer after Android has been replaced by a bare-metal kernel.

## QEMU emulation (2026-10-15)
- `tools/mkadt.py OUT.adt --qemu` = same ADT with QEMU virt GICD 0x08000000 / GICR 0x080a0000 / CNTFRQ 62.5 MHz.
- `tools/qemu-sweet.py PAYLOAD OUTDIR [--secs N] [--hmp "x /8gx ADDR"] [--gdb]`: host-side copy of shim/loader.c
  (segments + ADT + boot_args at their PAs, 6-instruction stub sets x0 and jumps), `-M virt,gic-version=3 -cpu cortex-a76`
  (same ID_AA64MMFR0 as Kryo 470), 4G RAM so 0x9c000000 fb and 0xb0000000 kernel are plain RAM.
  Outputs `fb.png` (the screen), `regs.txt`, `qemu.log` (exceptions with ESR/FAR/ELR). `--gdb` halts with a stub on :1234
  (system `gdb` + `set architecture aarch64`, `hbreak *VA` works with the MMU on).
- Not emulated: Qualcomm XPUs, ABL, real panel, PSCI conduit (QEMU virt uses hvc). Hardware still decides those.
- Example: `python3 tools/mkadt.py /tmp/q.adt --qemu && python3 tools/mkpayload.py xnu/out-0013/kernel.development.sweet /tmp/q.adt /tmp/pq.bin --cmdline 'debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam' && python3 tools/qemu-sweet.py /tmp/pq.bin /tmp/q`

## Layout
- `backup/`  partition dumps + full sdb..sdf LUNs, `SHA256SUMS` (all verified on-device == local)
- `dtb/`     live FDT (from OrangeFox), PixelOS boot.img dtb, dtbo, dts versions
- `shim/`    bare-metal boot shim (`./build.sh` -> `out/shim-boot.img`)
- `research/` mainline sm7150 dts, XNU pe_fiq.c etc, PocketDarwin patches
- `tools/unpack_bootv2.py`

## Device access
- No root in PixelOS 17 (user build, adb root disabled). Root = `fastboot boot recovery/recovery.img` (OrangeFox R12.0_2, temp boot, not flashed).
- `fastboot boot` works for stock boot.img, OrangeFox, and our shim.
- Shim resets itself via PSCI SYSTEM_RESET; IMEM restart_reason 0x77665500 is seen
  (bootreason=bootloader) but ABL still boots Android, so it does not stop in fastboot.

## Hardware facts (live DT + shim measurements)
- Framebuffer (ABL cont splash): 0x9c000000, 1080x2400, stride 4320, a8r8g8b8, panel is DSC *video* mode (no kick needed).
- RAM: 0x80000000+2G, 0x100000000+0xfcc00000. Live reserved-memory = PixelOS base dtb + sweet dtbo fixups.
- GICv3: GICD 0x17a00000, GICR 0x17a60000 (stride 0x20000, 8 PEs). GICD_TYPER 0x007B041D: SecurityExtn=1 (DS=0).
  ABL leaves GICD_CTLR = 0x10 (ARE_NS on, groups off). Writing 0x13 reads back 0x12: EnableGrp1A (bit1) is the one that matters.
- GIC Group 1 VERIFIED (shim 2c): vtimer INTID 19 = 30 IRQs/300ms, ptimer INTID 18 = 30, SGI 1 to self = 10/10.
  ICC_SRE=1 already, ICC_CTLR 0x8440, priority/enable writes stick. GICR_IGROUPR0 and GICD_IGROUPRn read 0 from NS
  even though Group 1 delivery works (RAZ in NS view) - do not use them as a health check.
  INTID 28 shows pending constantly (unknown PPI 12).
- Timer 19.2 MHz. Qualcomm PPI numbering: secure-phys/phys/virt/hyp = PPI 1/2/3/0 -> vtimer INTID 19, ptimer 18 (NOT 27/30).
- PSCI 1.1 via SMC, SMCCC 1.1. CPU_ON ok; SYSTEM_SUSPEND and SYSTEM_RESET2 unsupported.
- SMP: CPU_ON works for all 7 secondaries (MPIDR 0x81000n00).
- Entry EL1, MMU off, x0 = DTB (magic ok). ID_AA64MMFR0 = ...101122: 16K granule YES, 4K YES.
- No serial console: debug UART SE is in SPI mode on sweet. Screen is the only debug channel.

## XNU implications
- XNU GICv3 path (pexpert/arm/pe_fiq.c, VMAPPLE) puts the timer (PPI 27) in Group 0 = FIQ. With SecurityExtn=1,
  Group 0 is secure -> impossible from NS EL1. Need: Group 1 IRQ, ICC_IGRPEN1, INTID 19, and the timer handled in the IRQ path.
- XNU VMAPPLE PSCI uses `hvc`; sweet needs `smc`.
- PocketDarwin NonAppleGenericCpu.patch only swaps -mcpu=apple-h7 for -march=armv8-a.

## Milestone 3 (2026-10-14): 16K MMU verified
- ABL loads the Image at 0x80080000 (base 0x80000000 + 0x80000) regardless of text_offset=0.
- 16K granule, T0SZ=28 (L2 start, 32MB blocks), MAIR 0x44ff00, TCR 0x1409CB51C, PARange=2 (40-bit PA).
- Only own image pages WB (Qualcomm XPUs: never map carve-outs cacheable); fb Normal-NC; rest Device.
- AT S1E1R checks all as expected; unmapped -> translation fault L2.
- Fill fb: 110 ms (MMU off) -> 3.5 ms (NC). Memory loop 70 ms -> 0.7 ms. vtimer + SGI IRQs still fine with MMU on.

## XNU loader design notes (xnu-8796)
- Entry: `_start` -> `start_first_cpu`, x0 = boot_args (PA), MMU off, EL1. boot_args: Revision/Version 2,
  virtBase/physBase/memSize/topOfKernelData, Boot_Video (fb 0x9c000000, rowBytes 4320, 1080x2400, depth 32),
  deviceTreeP/Length (ADT), CommandLine[608], bootFlags, memSizeActual.
- start.s maps [kernel mach header .. physBase+memSize) with cacheable BLOCKS. On Qualcomm every XPU carve-out
  must therefore lie below the kernel: use physBase = 0xb0000000 (above ramdump_fb 0xaf000000+16M,
  cdsp_sec, qseecom), end before rmtfs 0xfde01000 -> memSize ~0x4d000000 for bring-up.
- Base ADT: iPhone 8 d20ap DeviceTree from iOS 16.7.16 IPSW (tools/remotezip.py + tools/adt.py; LZFSE payload).
  Template values are empty: the loader must fill chosen/*, memory-map, cpu*/reg etc. like iBoot.
- XNU build: GitHub Actions (dipa-studio/ios-sweet, xnu.yml) via blacktop/darwin-xnu-build, MACOS_VERSION=13.5.
  New-clang fixes in xnu/patches; Xcode 16 iig is incompatible (IORPC.kernelContent) -> macos-14 runner, oldest Xcode.

## Kernel architecture plan (SWEET machine config)
- First stock build (VMAPPLE) is arm64e (PAC). Kryo 470 = ARMv8.2, no PAC -> SWEET must build plain arm64
  (HAS_APPLE_PAC is only defined for __arm64e__, so arm64 drops PAC automatically).
- Template: VMAPPLE (16K pages, GICv3 code in pe_fiq.c) minus APPLEVIRTUALPLATFORM hypercalls/paravirt PAC,
  plus BCM2837 (generic ARM: no APPLE_ARM64_ARCH_FAMILY Apple sysregs). Do not link the KDK lib<cfg>.os.*.a.
- Timer: XNU expects it on FIQ (sleh_fiq -> rtclock_intr). SWEET: GIC Group 1, so sleh_irq must ack ICC_IAR1,
  route INTID 19 to the same timer path, SGIs to cpu_signal_handler, EOI via ICC_EOIR1.
- SMP/interrupts: open-source AppleARMSMP (USE_APPLEARMSMP) needs an IOInterruptController (AIC role) and an
  IOPMGR (CPU power -> PSCI CPU_ON via SMC). Plan: built-in IOKit classes (SweetGIC, SweetPMGR, platform
  expert) compiled into the kernel and matched via iokit/KernelConfigTables.cpp -> no closed kexts needed.
- Debug: xnu patch 0003 sweet-fbcon = kprintf drawn on the framebuffer (ADT node "sweet-fbcon").
- ADT /arm-io ranges must not map to parent 0 (pe_arm_get_soc_base_phys()==0 disables serial): use parent 0x1000000.

## Status 2026-10-14 late: first XNU boot attempt
- SWEET kernel builds (CI run 38635343732, patches 0001-0009). Verified offline: arm64, no PAC, no >v8.2 code,
  70300 classic relocs all in range (slide 0 = no loader work), entry = __start.
- Boot: shim loader worked (initrd 0x846F0000-0x855FE3E0, BOOTARG 0xB1FF8000, JUMP 0xB146A488) but screen stayed
  red -> xnu died/hung before serial_init (fbcon). kprintf is a no-op before STARTUP_SUB_KPRINTF.
- Historical next-step plan (patch 0010, now implemented and built; see active handoff above): early fb debug channel
  1. start.s start_first_cpu (after mov x20,x0 / mov x21,#0): PA marker band (MMU off, direct store to 0x9c000000).
  2. start.s after both create_bootstrap_mapping calls: add ONE block entry to the existing V=P L2 table
     (x25 + 2*PGBYTES; do NOT call create_bootstrap_mapping again: fb and RAM share L1 entry 0, it would replace
     the L2 table). Entry = TYPE_BLOCK|VALID|SH(OUTER)|ATTRINDX(CACHE_ATTRINDX_WRITECOMB=1)|AF|PNX|NX|0x9c000000,
     index = (va & ARM_TT_L2_INDEX_MASK) >> ARM_TT_L2_SHIFT.
  3. new osfmk/arm64/sweet_early.c (+files.arm64 entry): sweet_early_mark(n) colored bands at screen bottom and
     sweet_early_putc using iso_font via VA=PA while the bootstrap TTBR0 is live; disable before
     arm_vm_init's set_mmu_ttb(invalid_ttep) (arm_vm_init.c:2148).
  4. markers in arm_init after PE_init_platform, ml_parse_cpu_topology, cpu_bootstrap, kernel_startup_bootstrap,
     cpu_init, before arm_vm_init.
  5. panic hook at top of panic_trap_to_debugger: va_copy + _doprnt(fmt, &copy, sweet_early_putc, 16).
  Verify with tools/xnu-cc.py (compile+symbols) and patch-order simulation before the single CI run.


## Read-only discussion / external research checkpoint (2026-10-21)

- User requested analysis of chat 01a158d0-9239-7503-baf3-10373eab7eff and
  online comparable solutions. This discussion performed no phone IO, build,
  runtime-source edits or messages to the active chat. Active handoff above
  remains authoritative; another chat is building the measured120s candidate.
- Independently read scalar pmsg: native prepare rc=-8, stream1, completed
  26738688 of38456840 bytes at20.0516883s. This establishes budget exhaustion
  before RAM Linux for that trial, not a hash mismatch or XNU crash. ~1.2717
  MiB/s is an aggregate observed rate, not a proved CPU/cache bottleneck.
- Public primary references inspected: https://github.com/dipa-studio/ios-sweet
  and https://github.com/MakrSas/ios-topaz provide Qualcomm platform work;
  neither is a verified PGKM10/MT6895 solution. https://t.me/s/oosexgangdevs
  says publication follows rewriting/polishing; no reproducible MT6895 fix
  was located in this search. Channel claims do not establish physical success.
- Linux v6.6 arch/arm64/crypto/sha2-ce-glue.c explicitly checks SIMD usability
  and brackets CE with kernel_neon_begin/end. Native EL1 requires its own
  feature/trap/state/alignment proof; Android CE use does not establish it.
- Advisory: first test the single measured-budget change with complete hash,
  layout and latch checks retained; record stage/elapsed/progress and independently
  prove RAM recovery before longer root writes. Treat ~73s two-pass estimate
  and120s headroom as estimates awaiting physical validation. Cache/MMU/CE and
  direct firmware-return changes should be separate experiments. No iOS GUI,
  touch or actual usability established by this research.
