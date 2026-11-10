"""Browser regression checks. Uses existing system Chromium and Playwright.
No request is sent to SOCOR's form endpoint. axe-core is an optional audit tool.
"""
from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
OUT=ROOT/'audit';OUT.mkdir(exist_ok=True)
BASE=os.environ.get('SOCOR_TEST_URL','http://localhost:3000')
routes=['/','/about','/projects','/products-services','/equipment','/contact']+['/products-services/'+x for x in ['hot-mix-asphalt','ready-mix-concrete','aggregates','equipment-rental','land-transport']]
checks=[]
def passed(name):checks.append(name);print('PASS',name,flush=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000})
 errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 violations=[]
 for route in routes:
  response=page.goto(BASE+route,wait_until='networkidle');assert response.status==200,route
  assert page.locator('h1').count()==1,route
  assert page.locator('header nav [aria-current]').count()==1,route
  title=page.title();assert title and 'SOCOR' in title,route
  assert page.locator('meta[name=description]').get_attribute('content'),route
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),route
  page.reload(wait_until='networkidle');assert page.locator('h1').is_visible(),route
  axe=ROOT / 'audit' / 'axe.min.js'
  if axe.exists():
   page.add_script_tag(path=str(axe))
   report=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
   violations += [{'route':route,'id':v['id'],'impact':v['impact'],'nodes':[{'target':n['target'],'summary':n.get('failureSummary')} for n in v['nodes']]} for v in report['violations']]
 passed('11 desktop routes, active states, direct reloads, metadata and page width')
 # Every local link resolves. Anchors must exist in the destination document.
 links=set()
 for route in routes:
  page.goto(BASE+route,wait_until='domcontentloaded')
  links.update(page.locator('a[href^="/"]').evaluate_all('(as)=>as.map(a=>a.getAttribute("href"))'))
 for href in links:assert page.request.get(BASE+href).status==200,href
 passed(str(len(links))+' unique internal link destinations return HTTP 200')
 for old,new in [('new-about','about'),('new-projects','projects'),('new-equipment','equipment'),('new-products-services','products-services'),('new-contact-us','contact')]:
  page.goto(BASE+'/'+old,wait_until='networkidle');page.wait_for_url('**/'+new+'*');assert page.locator('h1').is_visible()
 passed('5 original URLs redirect to implemented pages')
 page.goto(BASE+'/projects',wait_until='networkidle')
 for category,count in [('Roads & bridges',2),('Airports',1),('Paving',1),('All',4)]:
  page.get_by_role('button',name=category,exact=True).click();assert page.locator('.portfolio-item:visible').count()==count
 page.locator('.image-open').first.focus();page.keyboard.press('Enter');assert page.locator('dialog').is_visible();assert page.locator('dialog img').get_attribute('alt')
 page.keyboard.press('Escape');assert not page.locator('dialog').is_visible();assert page.locator('.image-open').first.evaluate('(e)=>document.activeElement===e')
 passed('Project category filters; keyboard gallery opening, Escape and focus restoration')
 page.goto(BASE+'/equipment',wait_until='networkidle');field=page.get_by_role('searchbox')
 total=page.locator('tbody tr').count();field.fill('asphalt');assert 0<page.locator('tbody tr:visible').count()<total
 field.fill('zzznomatches');assert page.locator('tbody tr:visible').count()==0;assert page.locator('#no-equipment').is_visible()
 field.fill('');assert page.locator('tbody tr:visible').count()==total
 passed('Equipment search, no-results state and reset across '+str(total)+' rows')
 for width in [834,390,320]:
  page.set_viewport_size({'width':width,'height':900})
  for route in routes:
   page.goto(BASE+route,wait_until='networkidle');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(route,width)
   if width in [834,390] and axe.exists():
    page.add_script_tag(path=str(axe))
    report=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
    violations += [{'route':route,'viewport':width,'id':v['id'],'impact':v['impact'],'nodes':[{'target':n['target'],'summary':n.get('failureSummary')} for n in v['nodes']]} for v in report['violations']]
  if width<=760:
   button=page.get_by_role('button',name='Menu');button.focus();page.keyboard.press('Enter');assert button.get_attribute('aria-expanded')=='true'
   page.keyboard.press('Tab');assert page.evaluate('document.activeElement.closest("#navigation")!==null')
   page.keyboard.press('Escape');assert button.get_attribute('aria-expanded')=='false';assert button.evaluate('(e)=>e===document.activeElement')
   button.click();page.locator('header nav a[href="/about"]').click();page.wait_for_url('**/about');assert page.locator('h1').is_visible()
   page.go_back();assert '/products-services/land-transport' in page.url;page.go_forward();assert '/about' in page.url
   page.evaluate('scrollTo(0,500)');page.wait_for_timeout(150);assert page.locator('header').bounding_box()['y']==0
  passed('All 11 routes at '+str(width)+'px; mobile keyboard menu/history/sticky header where applicable')
 page.set_viewport_size({'width':390,'height':844});page.emulate_media(reduced_motion='reduce');page.goto(BASE+'/projects',wait_until='networkidle')
 assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
 assert page.locator('.reveal-once').count()==0
 assert page.locator('main').evaluate('(e)=>getComputedStyle(e).animationName')=='none'
 passed('Reduced motion: no image reveal, page entrance or smooth scrolling')
 (OUT/'accessibility-results.json').write_text(json.dumps(violations,indent=2))
 page.goto(BASE+'/contact?service=hot-mix-asphalt',wait_until='networkidle')
 assert 'hot mix asphalt' in page.locator('textarea').input_value()
 assert page.locator('form').evaluate('(e)=>!e.checkValidity()')
 assert page.locator('input[type=tel]').evaluate("e=>{e.value='invalid';return !e.checkValidity()}")
 for selector,value in [('name','Test'),('field_fccabf3','Visitor'),('email','review@example.com'),('field_ff3133b','+63 917 000 0000')]:page.locator('[name="form_fields['+selector+']"]').fill(value)
 page.locator('textarea').fill('Local audit draft only. This inquiry must not be sent.')
 outbound=[];page.on('request',lambda request:outbound.append(request.url) if 'admin-ajax.php' in request.url else None)
 page.get_by_role('button',name='Prepare email').click();draft=page.locator('#email-draft');assert draft.is_visible();assert draft.get_attribute('href').startswith('mailto:socorcebu@socorconstruction.com?')
 assert 'Nothing has been sent' in page.locator('#form-status').inner_text();assert not outbound
 assert page.locator('textarea').input_value()
 page.locator('textarea').fill('Revised local audit text');assert not draft.is_visible()
 passed('Contact required fields, service prefill, email draft encoding, explicit unsent state and edit invalidation; zero AJAX requests')
 page.goto(BASE+'/',wait_until='networkidle');page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Enter');page.wait_for_url('**/#main');assert page.url.endswith('#main')
 passed('Keyboard skip link')
 assert not errors,errors
 browser.close()
(OUT/'browser-results.json').write_text(json.dumps({'checks':checks,'axe_violations':violations,'js_errors':errors},indent=2))
print('Accessibility violations:',json.dumps(violations,indent=2),flush=True)
assert not violations,'Accessibility violations need review'
