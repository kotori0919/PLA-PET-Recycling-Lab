from pathlib import Path
import json
E=Path('/home/monad/develop/PPR/experiments/hot_slide_r1')
p=E/'package_review.py';s=p.read_text()
old="    test=json.loads((ROOT/'protocol_test_results.json').read_text());assert test['status']=='PASS' and test['count']==26"
new="""    test_suites = [('test_protocol.py', 'protocol_test_results.json', 26), ('test_protocol_boundaries.py', 'protocol_boundary_results.json', 25)]
    test_count = 0
    for script, report_name, expected_count in test_suites:
        execution = subprocess.run([sys.executable, str(ROOT/script)], cwd=ROOT, capture_output=True, text=True, timeout=60)
        if execution.returncode: raise RuntimeError('Protocol regression failed: ' + script)
        report = json.loads((ROOT/report_name).read_text())
        if report.get('status') != 'PASS' or report.get('count') != expected_count or report.get('kind') != 'SYNTHETIC_SOFTWARE_TESTS_ONLY': raise RuntimeError('Invalid synthetic test evidence')
        test_count += report['count']
    template = json.loads((ROOT/'physical_test_template.json').read_text())
    if template.get('performed') is not False or template.get('samples') != []: raise RuntimeError('Refuse to package measured data as a blank template')"""
assert s.count(old)==1;s=s.replace(old,new)
old="    paths=[p for p in ROOT.iterdir() if p.is_file() and p.suffix in allowed and p.name not in {'package_manifest.json','package_final_check.json'}]"
names=sorted({n for n in json.loads((E/'package_manifest.json').read_text())['files'] if '/' not in n and n!='HS-R1-S2_prototype_review_ko_v2.pdf'}|{'update_scoped_graph.py','test_protocol_boundaries.py','protocol_boundary_results.json','COLD_TEST_READINESS_KO.md'})
new='    root_names = '+repr(names)+'\n    paths = [ROOT/name for name in root_names]\n    paths += [ROOT/"graphify-out"/name for name in ("GRAPH_REPORT.md","manifest.json","cost.json")]'
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("'source_head':","'generation_base_git_sha':").replace("'unit_tests':26","'unit_tests':test_count").replace("'unit_tests':test['count']","'unit_tests':test_count")
s=s.replace('PPR-HS-R1-S2-TEST-FOUNDATION-20260909.zip','PPR-HS-R1-S2-TEST-FOUNDATION-20260909-r1.zip')
s=s.replace("'physical_validation':'NOT_RUN','generation_base_git_sha'","'physical_validation':'NOT_RUN','record_protocol_revision':'20260909-r1','read_first':'COLD_TEST_READINESS_KO.md','generation_base_git_sha'")
compile(s,str(p),'exec');p.write_text(s)
print('PACKAGE_UPDATED',len(names))
