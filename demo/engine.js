(function dartProgram(){function copyProperties(a,b){var t=Object.keys(a)
for(var s=0;s<t.length;s++){var r=t[s]
b[r]=a[r]}}function mixinPropertiesHard(a,b){var t=Object.keys(a)
for(var s=0;s<t.length;s++){var r=t[s]
if(!b.hasOwnProperty(r)){b[r]=a[r]}}}function mixinPropertiesEasy(a,b){Object.assign(b,a)}var z=function(){var t=function(){}
t.prototype={p:{}}
var s=new t()
if(!(Object.getPrototypeOf(s)&&Object.getPrototypeOf(s).p===t.prototype.p))return false
try{if(typeof navigator!="undefined"&&typeof navigator.userAgent=="string"&&navigator.userAgent.indexOf("Chrome/")>=0)return true
if(typeof version=="function"&&version.length==0){var r=version()
if(/^\d+\.\d+\.\d+\.\d+$/.test(r))return true}}catch(q){}return false}()
function inherit(a,b){a.prototype.constructor=a
a.prototype["$i"+a.name]=a
if(b!=null){if(z){Object.setPrototypeOf(a.prototype,b.prototype)
return}var t=Object.create(b.prototype)
copyProperties(a.prototype,t)
a.prototype=t}}function inheritMany(a,b){for(var t=0;t<b.length;t++){inherit(b[t],a)}}function mixinEasy(a,b){mixinPropertiesEasy(b.prototype,a.prototype)
a.prototype.constructor=a}function mixinHard(a,b){mixinPropertiesHard(b.prototype,a.prototype)
a.prototype.constructor=a}function lazy(a,b,c,d){var t=a
a[b]=t
a[c]=function(){if(a[b]===t){a[b]=d()}a[c]=function(){return this[b]}
return a[b]}}function lazyFinal(a,b,c,d){var t=a
a[b]=t
a[c]=function(){if(a[b]===t){var s=d()
if(a[b]!==t){A.ij(b)}a[b]=s}var r=a[b]
a[c]=function(){return r}
return r}}function makeConstList(a,b){if(b!=null)A.t(a,b)
a.$flags=7
return a}function convertToFastObject(a){function t(){}t.prototype=a
new t()
return a}function convertAllToFastObject(a){for(var t=0;t<a.length;++t){convertToFastObject(a[t])}}var y=0
function instanceTearOffGetter(a,b){var t=null
return a?function(c){if(t===null)t=A.e2(b)
return new t(c,this)}:function(){if(t===null)t=A.e2(b)
return new t(this,null)}}function staticTearOffGetter(a){var t=null
return function(){if(t===null)t=A.e2(a).prototype
return t}}var x=0
function tearOffParameters(a,b,c,d,e,f,g,h,i,j){if(typeof h=="number"){h+=x}return{co:a,iS:b,iI:c,rC:d,dV:e,cs:f,fs:g,fT:h,aI:i||0,nDA:j}}function installStaticTearOff(a,b,c,d,e,f,g,h){var t=tearOffParameters(a,true,false,c,d,e,f,g,h,false)
var s=staticTearOffGetter(t)
a[b]=s}function installInstanceTearOff(a,b,c,d,e,f,g,h,i,j){c=!!c
var t=tearOffParameters(a,false,c,d,e,f,g,h,i,!!j)
var s=instanceTearOffGetter(c,t)
a[b]=s}function setOrUpdateInterceptorsByTag(a){var t=v.interceptorsByTag
if(!t){v.interceptorsByTag=a
return}copyProperties(a,t)}function setOrUpdateLeafTags(a){var t=v.leafTags
if(!t){v.leafTags=a
return}copyProperties(a,t)}function updateTypes(a){var t=v.types
var s=t.length
t.push.apply(t,a)
return s}function updateHolder(a,b){copyProperties(b,a)
return a}var hunkHelpers=function(){var t=function(a,b,c,d,e){return function(f,g,h,i){return installInstanceTearOff(f,g,a,b,c,d,[h],i,e,false)}},s=function(a,b,c,d){return function(e,f,g,h){return installStaticTearOff(e,f,a,b,c,[g],h,d)}}
return{inherit:inherit,inheritMany:inheritMany,mixin:mixinEasy,mixinHard:mixinHard,installStaticTearOff:installStaticTearOff,installInstanceTearOff:installInstanceTearOff,_instance_0u:t(0,0,null,["$0"],0),_instance_1u:t(0,1,null,["$1"],0),_instance_2u:t(0,2,null,["$2"],0),_instance_0i:t(1,0,null,["$0"],0),_instance_1i:t(1,1,null,["$1"],0),_instance_2i:t(1,2,null,["$2"],0),_static_0:s(0,null,["$0"],0),_static_1:s(1,null,["$1"],0),_static_2:s(2,null,["$2"],0),makeConstList:makeConstList,lazy:lazy,lazyFinal:lazyFinal,updateHolder:updateHolder,convertToFastObject:convertToFastObject,updateTypes:updateTypes,setOrUpdateInterceptorsByTag:setOrUpdateInterceptorsByTag,setOrUpdateLeafTags:setOrUpdateLeafTags}}()
function initializeDeferredHunk(a){x=v.types.length
a(hunkHelpers,v,w,$)}var J={
e6(a,b,c,d){return{i:a,p:b,e:c,x:d}},
dx(a){var t,s,r,q,p,o="_$dart_js",n=a[v.dispatchPropertyName]
if(n==null)if($.e4==null){A.i7()
n=a[v.dispatchPropertyName]}if(n!=null){t=n.p
if(!1===t)return n.i
if(!0===t)return a
s=Object.getPrototypeOf(a)
if(t===s)return n.i
if(n.e===s)throw A.a(A.ew("Return interceptor for "+A.l(t(a,n))))}r=a.constructor
if(r==null)q=null
else{p=$.d3
if(p==null)p=$.d3=A.dw(o)
q=r[p]}if(q!=null)return q
q=A.ic(a)
if(q!=null)return q
if(typeof a=="function")return B.a2
t=Object.getPrototypeOf(a)
if(t==null)return B.N
if(t===Object.prototype)return B.N
if(typeof r=="function"){p=$.d3
if(p==null)p=$.d3=A.dw(o)
Object.defineProperty(r,p,{value:B.y,enumerable:false,writable:true,configurable:true})
return B.y}return B.y},
el(a,b){if(a<0||a>4294967295)throw A.a(A.a6(a,0,4294967295,"length",null))
return J.fC(new Array(a),b)},
fC(a,b){var t=A.t(a,b.i("o<0>"))
t.$flags=1
return t},
fD(a,b){var t=u.W
return J.fm(t.a(a),t.a(b))},
ar(a){if(typeof a=="number"){if(Math.floor(a)==a)return J.bd.prototype
return J.c6.prototype}if(typeof a=="string")return J.az.prototype
if(a==null)return J.be.prototype
if(typeof a=="boolean")return J.c5.prototype
if(Array.isArray(a))return J.o.prototype
if(typeof a!="object"){if(typeof a=="function")return J.a9.prototype
if(typeof a=="symbol")return J.aX.prototype
if(typeof a=="bigint")return J.aV.prototype
return a}if(a instanceof A.m)return a
return J.dx(a)},
A(a){if(typeof a=="string")return J.az.prototype
if(a==null)return a
if(Array.isArray(a))return J.o.prototype
if(typeof a!="object"){if(typeof a=="function")return J.a9.prototype
if(typeof a=="symbol")return J.aX.prototype
if(typeof a=="bigint")return J.aV.prototype
return a}if(a instanceof A.m)return a
return J.dx(a)},
U(a){if(a==null)return a
if(Array.isArray(a))return J.o.prototype
if(typeof a!="object"){if(typeof a=="function")return J.a9.prototype
if(typeof a=="symbol")return J.aX.prototype
if(typeof a=="bigint")return J.aV.prototype
return a}if(a instanceof A.m)return a
return J.dx(a)},
i3(a){if(typeof a=="number")return J.aU.prototype
if(typeof a=="string")return J.az.prototype
if(a==null)return a
if(!(a instanceof A.m))return J.b0.prototype
return a},
e3(a){if(a==null)return a
if(typeof a!="object"){if(typeof a=="function")return J.a9.prototype
if(typeof a=="symbol")return J.aX.prototype
if(typeof a=="bigint")return J.aV.prototype
return a}if(a instanceof A.m)return a
return J.dx(a)},
v(a,b){if(a==null)return b==null
if(typeof a!="object")return b!=null&&a===b
return J.ar(a).R(a,b)},
f(a,b){if(typeof b==="number")if(Array.isArray(a)||typeof a=="string"||A.ia(a,a[v.dispatchPropertyName]))if(b>>>0===b&&b<a.length)return a[b]
return J.A(a).h(a,b)},
fj(a,b,c){return J.U(a).A(a,b,c)},
dI(a){return J.e3(a).aJ(a)},
fk(a,b,c){return J.e3(a).a1(a,b,c)},
fl(a){return J.e3(a).aK(a)},
bP(a,b){return J.U(a).a2(a,b)},
fm(a,b){return J.i3(a).aL(a,b)},
bQ(a,b){return J.U(a).B(a,b)},
dJ(a,b){return J.U(a).u(a,b)},
fn(a,b){return J.U(a).ai(a,b)},
fo(a){return J.U(a).gE(a)},
a2(a){return J.ar(a).gv(a)},
fp(a){return J.A(a).gt(a)},
ea(a){return J.U(a).gJ(a)},
cy(a){return J.U(a).gp(a)},
fq(a){return J.U(a).gF(a)},
aN(a){return J.A(a).gj(a)},
fr(a){return J.ar(a).gG(a)},
eb(a,b,c){return J.U(a).U(a,b,c)},
dK(a,b){return J.U(a).L(a,b)},
ec(a){return J.U(a).H(a)},
aj(a){return J.ar(a).k(a)},
c3:function c3(){},
c5:function c5(){},
be:function be(){},
bf:function bf(){},
am:function am(){},
ce:function ce(){},
b0:function b0(){},
a9:function a9(){},
aV:function aV(){},
aX:function aX(){},
o:function o(a){this.$ti=a},
c4:function c4(){},
cG:function cG(a){this.$ti=a},
as:function as(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
aU:function aU(){},
bd:function bd(){},
c6:function c6(){},
az:function az(){}},A={dM:function dM(){},
dL(a,b,c){if(u.O.b(a))return new A.bB(a,b.i("@<0>").q(c).i("bB<1,2>"))
return new A.at(a,b.i("@<0>").q(c).i("at<1,2>"))},
fF(a){return new A.aY("Field '"+a+"' has not been initialized.")},
fE(a){return new A.aY("Field '"+a+"' has already been initialized.")},
ag(a,b){a=a+b&536870911
a=a+((a&524287)<<10)&536870911
return a^a>>>6},
cZ(a){a=a+((a&67108863)<<3)&536870911
a^=a>>>11
return a+((a&16383)<<15)&536870911},
e5(a){var t,s
for(t=$.T.length,s=0;s<t;++s)if(a===$.T[s])return!0
return!1},
cY(a,b,c,d){A.V(b,"start")
if(c!=null){A.V(c,"end")
if(b>c)A.i(A.a6(b,0,c,"start",null))}return new A.bx(a,b,c,d.i("bx<0>"))},
fI(a,b,c,d){if(u.O.b(a))return new A.aw(a,b,c.i("@<0>").q(d).i("aw<1,2>"))
return new A.aD(a,b,c.i("@<0>").q(d).i("aD<1,2>"))},
et(a,b,c){var t="count"
if(u.O.b(a)){A.cz(b,t,u.S)
A.V(b,t)
return new A.aS(a,b,c.i("aS<0>"))}A.cz(b,t,u.S)
A.V(b,t)
return new A.ae(a,b,c.i("ae<0>"))},
C(){return new A.aZ("No element")},
ek(){return new A.aZ("Too few elements")},
an:function an(){},
b8:function b8(a,b){this.a=a
this.$ti=b},
at:function at(a,b){this.a=a
this.$ti=b},
bB:function bB(a,b){this.a=a
this.$ti=b},
bA:function bA(){},
a8:function a8(a,b){this.a=a
this.$ti=b},
au:function au(a,b){this.a=a
this.$ti=b},
cA:function cA(a,b){this.a=a
this.b=b},
aY:function aY(a){this.a=a},
cP:function cP(){},
k:function k(){},
D:function D(){},
bx:function bx(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.$ti=d},
aB:function aB(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
aD:function aD(a,b,c){this.a=a
this.b=b
this.$ti=c},
aw:function aw(a,b,c){this.a=a
this.b=b
this.$ti=c},
bk:function bk(a,b,c){var _=this
_.a=null
_.b=a
_.c=b
_.$ti=c},
R:function R(a,b,c){this.a=a
this.b=b
this.$ti=c},
ae:function ae(a,b,c){this.a=a
this.b=b
this.$ti=c},
aS:function aS(a,b,c){this.a=a
this.b=b
this.$ti=c},
bv:function bv(a,b,c){this.a=a
this.b=b
this.$ti=c},
ax:function ax(a){this.$ti=a},
bb:function bb(a){this.$ti=a},
ay:function ay(){},
bM:function bM(){},
fA(){throw A.a(A.b1("Cannot modify constant Set"))},
f4(a){var t=A.f3(a)
if(t!=null)return t
return"minified:"+a},
ia(a,b){var t
if(b!=null){t=b.x
if(t!=null)return t}return u.p.b(a)},
l(a){var t
if(typeof a=="string")return a
if(typeof a=="number"){if(a!==0)return""+a}else if(!0===a)return"true"
else if(!1===a)return"false"
else if(a==null)return"null"
t=J.aj(a)
return t},
br(a){var t,s=$.eq
if(s==null)s=$.eq=Symbol("identityHashCode")
t=a[s]
if(t==null){t=Math.random()*0x3fffffff|0
a[s]=t}return t},
cf(a){var t,s,r,q
if(a instanceof A.m)return A.S(A.a0(a),null)
t=J.ar(a)
if(t===B.a1||t===B.a3||u.o.b(a)){s=B.H(a)
if(s!=="Object"&&s!=="")return s
r=a.constructor
if(typeof r=="function"){q=r.name
if(typeof q=="string"&&q!=="Object"&&q!=="")return q}}return A.S(A.a0(a),null)},
er(a){var t,s,r
if(a==null||typeof a=="number"||A.e_(a))return J.aj(a)
if(typeof a=="string")return JSON.stringify(a)
if(a instanceof A.ak)return a.k(0)
if(a instanceof A.ao)return a.aI(!0)
t=$.fi()
for(s=0;s<1;++s){r=t[s].bB(a)
if(r!=null)return r}return"Instance of '"+A.cf(a)+"'"},
fN(a,b,c){var t,s,r,q
if(c<=500&&b===0&&c===a.length)return String.fromCharCode.apply(null,a)
for(t=b,s="";t<c;t=r){r=t+500
q=r<c?r:c
s+=String.fromCharCode.apply(null,a.subarray(t,q))}return s},
K(a){var t
if(a<=65535)return String.fromCharCode(a)
if(a<=1114111){t=a-65536
return String.fromCharCode((B.f.aH(t,10)|55296)>>>0,t&1023|56320)}throw A.a(A.a6(a,0,1114111,null,null))},
bN(a){throw A.a(A.hV(a))},
d(a,b){if(a==null)J.aN(a)
throw A.a(A.cw(a,b))},
cw(a,b){var t,s="index"
if(!A.eR(b))return new A.a3(!0,b,s,null)
t=J.aN(a)
if(b<0||b>=t)return A.c2(b,t,a,null,s)
return A.fP(b,s)},
i0(a,b,c){if(a>c)return A.a6(a,0,c,"start",null)
if(b!=null)if(b<a||b>c)return A.a6(b,a,c,"end",null)
return new A.a3(!0,b,"end",null)},
hV(a){return new A.a3(!0,a,null,null)},
a(a){return A.G(a,new Error())},
G(a,b){var t
if(a==null)a=new A.by()
b.dartException=a
t=A.il
if("defineProperty" in Object){Object.defineProperty(b,"message",{get:t})
b.name=""}else b.toString=t
return b},
il(){return J.aj(this.dartException)},
i(a,b){throw A.G(a,b==null?new Error():b)},
M(a,b,c){var t
if(b==null)b=0
if(c==null)c=0
t=Error()
A.i(A.hr(a,b,c),t)},
hr(a,b,c){var t,s,r,q,p,o,n,m,l
if(typeof b=="string")t=b
else{s="[]=;add;removeWhere;retainWhere;removeRange;setRange;setInt8;setInt16;setInt32;setUint8;setUint16;setUint32;setFloat32;setFloat64".split(";")
r=s.length
q=b
if(q>r){c=q/r|0
q%=r}t=s[q]}p=typeof c=="string"?c:"modify;remove from;add to".split(";")[c]
o=u.j.b(a)?"list":"ByteData"
n=a.$flags|0
m="a "
if((n&4)!==0)l="constant "
else if((n&2)!==0){l="unmodifiable "
m="an "}else l=(n&1)!==0?"fixed-length ":""
return new A.bz("'"+t+"': Cannot "+p+" "+m+l+o)},
aM(a){throw A.a(A.N(a))},
ah(a){var t,s,r,q,p,o
a=A.ih(a.replace(String({}),"$receiver$"))
t=a.match(/\\\$[a-zA-Z]+\\\$/g)
if(t==null)t=A.t([],u.s)
s=t.indexOf("\\$arguments\\$")
r=t.indexOf("\\$argumentsExpr\\$")
q=t.indexOf("\\$expr\\$")
p=t.indexOf("\\$method\\$")
o=t.indexOf("\\$receiver\\$")
return new A.d_(a.replace(new RegExp("\\\\\\$arguments\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$argumentsExpr\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$expr\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$method\\\\\\$","g"),"((?:x|[^x])*)").replace(new RegExp("\\\\\\$receiver\\\\\\$","g"),"((?:x|[^x])*)"),s,r,q,p,o)},
d0(a){return function($expr$){var $argumentsExpr$="$arguments$"
try{$expr$.$method$($argumentsExpr$)}catch(t){return t.message}}(a)},
ev(a){return function($expr$){try{$expr$.$method$}catch(t){return t.message}}(a)},
dN(a,b){var t=b==null,s=t?null:b.method
return new A.c7(a,s,t?null:b.receiver)},
e8(a){if(a==null)return new A.cK(a)
if(typeof a!=="object")return a
if("dartException" in a)return A.aL(a,a.dartException)
return A.hT(a)},
aL(a,b){if(u.C.b(b))if(b.$thrownJsError==null)b.$thrownJsError=a
return b},
hT(a){var t,s,r,q,p,o,n,m,l,k,j,i,h
if(!("message" in a))return a
t=a.message
if("number" in a&&typeof a.number=="number"){s=a.number
r=s&65535
if((B.f.aH(s,16)&8191)===10)switch(r){case 438:return A.aL(a,A.dN(A.l(t)+" (Error "+r+")",null))
case 445:case 5007:A.l(t)
return A.aL(a,new A.bq())}}if(a instanceof TypeError){q=$.f7()
p=$.f8()
o=$.f9()
n=$.fa()
m=$.fd()
l=$.fe()
k=$.fc()
$.fb()
j=$.fg()
i=$.ff()
h=q.M(t)
if(h!=null)return A.aL(a,A.dN(A.L(t),h))
else{h=p.M(t)
if(h!=null){h.method="call"
return A.aL(a,A.dN(A.L(t),h))}else if(o.M(t)!=null||n.M(t)!=null||m.M(t)!=null||l.M(t)!=null||k.M(t)!=null||n.M(t)!=null||j.M(t)!=null||i.M(t)!=null){A.L(t)
return A.aL(a,new A.bq())}}return A.aL(a,new A.cl(typeof t=="string"?t:""))}if(a instanceof RangeError){if(typeof t=="string"&&t.indexOf("call stack")!==-1)return new A.bw()
t=function(b){try{return String(b)}catch(g){}return null}(a)
return A.aL(a,new A.a3(!1,null,null,typeof t=="string"?t.replace(/^RangeError:\s*/,""):t))}if(typeof InternalError=="function"&&a instanceof InternalError)if(typeof t=="string"&&t==="too much recursion")return new A.bw()
return a},
e7(a){if(a==null)return J.a2(a)
if(typeof a=="object")return A.br(a)
return J.a2(a)},
hW(a){if(typeof a=="number")return B.c.gv(a)
if(a instanceof A.cv)return A.br(a)
if(a instanceof A.ao)return a.gv(a)
return A.e7(a)},
i2(a,b){var t,s,r,q=a.length
for(t=0;t<q;t=r){s=t+1
r=s+1
b.A(0,a[t],a[s])}return b},
hA(a,b,c,d,e,f){u.Z.a(a)
switch(A.F(b)){case 0:return a.$0()
case 1:return a.$1(c)
case 2:return a.$2(c,d)
case 3:return a.$3(c,d,e)
case 4:return a.$4(c,d,e,f)}throw A.a(new A.d2("Unsupported number of arguments for wrapped closure"))},
hX(a,b){var t=a.$identity
if(!!t)return t
t=A.hY(a,b)
a.$identity=t
return t},
hY(a,b){var t
switch(b){case 0:t=a.$0
break
case 1:t=a.$1
break
case 2:t=a.$2
break
case 3:t=a.$3
break
case 4:t=a.$4
break
default:t=null}if(t!=null)return t.bind(a)
return function(c,d,e){return function(f,g,h,i){return e(c,d,f,g,h,i)}}(a,b,A.hA)},
fz(a1){var t,s,r,q,p,o,n,m,l,k,j=a1.co,i=a1.iS,h=a1.iI,g=a1.nDA,f=a1.aI,e=a1.fs,d=a1.cs,c=e[0],b=d[0],a=j[c],a0=a1.fT
a0.toString
t=i?Object.create(new A.ci().constructor.prototype):Object.create(new A.aO(null,null).constructor.prototype)
t.$initialize=t.constructor
s=i?function static_tear_off(){this.$initialize()}:function tear_off(a2,a3){this.$initialize(a2,a3)}
t.constructor=s
s.prototype=t
t.$_name=c
t.$_target=a
r=!i
if(r)q=A.ei(c,a,h,g)
else{t.$static_name=c
q=a}t.$S=A.fv(a0,i,h)
t[b]=q
for(p=q,o=1;o<e.length;++o){n=e[o]
if(typeof n=="string"){m=j[n]
l=n
n=m}else l=""
k=d[o]
if(k!=null){if(r)n=A.ei(l,n,h,g)
t[k]=n}if(o===f)p=n}t.$C=p
t.$R=a1.rC
t.$D=a1.dV
return s},
fv(a,b,c){if(typeof a=="number")return a
if(typeof a=="string"){if(b)throw A.a("Cannot compute signature for static tearoff.")
return function(d,e){return function(){return e(this,d)}}(a,A.ft)}throw A.a("Error in functionType of tearoff")},
fw(a,b,c,d){var t=A.eg
switch(b?-1:a){case 0:return function(e,f){return function(){return f(this)[e]()}}(c,t)
case 1:return function(e,f){return function(g){return f(this)[e](g)}}(c,t)
case 2:return function(e,f){return function(g,h){return f(this)[e](g,h)}}(c,t)
case 3:return function(e,f){return function(g,h,i){return f(this)[e](g,h,i)}}(c,t)
case 4:return function(e,f){return function(g,h,i,j){return f(this)[e](g,h,i,j)}}(c,t)
case 5:return function(e,f){return function(g,h,i,j,k){return f(this)[e](g,h,i,j,k)}}(c,t)
default:return function(e,f){return function(){return e.apply(f(this),arguments)}}(d,t)}},
ei(a,b,c,d){if(c)return A.fy(a,b,d)
return A.fw(b.length,d,a,b)},
fx(a,b,c,d){var t=A.eg,s=A.fu
switch(b?-1:a){case 0:throw A.a(new A.cg("Intercepted function with no arguments."))
case 1:return function(e,f,g){return function(){return f(this)[e](g(this))}}(c,s,t)
case 2:return function(e,f,g){return function(h){return f(this)[e](g(this),h)}}(c,s,t)
case 3:return function(e,f,g){return function(h,i){return f(this)[e](g(this),h,i)}}(c,s,t)
case 4:return function(e,f,g){return function(h,i,j){return f(this)[e](g(this),h,i,j)}}(c,s,t)
case 5:return function(e,f,g){return function(h,i,j,k){return f(this)[e](g(this),h,i,j,k)}}(c,s,t)
case 6:return function(e,f,g){return function(h,i,j,k,l){return f(this)[e](g(this),h,i,j,k,l)}}(c,s,t)
default:return function(e,f,g){return function(){var r=[g(this)]
Array.prototype.push.apply(r,arguments)
return e.apply(f(this),r)}}(d,s,t)}},
fy(a,b,c){var t,s
if($.ee==null)$.ee=A.ed("interceptor")
if($.ef==null)$.ef=A.ed("receiver")
t=b.length
s=A.fx(t,c,a,b)
return s},
e2(a){return A.fz(a)},
ft(a,b){return A.bL(v.typeUniverse,A.a0(a.a),b)},
eg(a){return a.a},
fu(a){return a.b},
ed(a){var t,s,r,q=new A.aO("receiver","interceptor"),p=Object.getOwnPropertyNames(q)
p.$flags=1
t=p
for(p=t.length,s=0;s<p;++s){r=t[s]
if(q[r]===a)return r}throw A.a(A.X("Field name "+a+" not found."))},
dw(a){return v.getIsolateTag(a)},
iI(a,b,c){Object.defineProperty(a,b,{value:c,enumerable:false,writable:true,configurable:true})},
ic(a){var t,s,r,q,p,o=A.L($.f0.$1(a)),n=$.dv[o]
if(n!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:n,enumerable:false,writable:true,configurable:true})
return n.i}t=$.dB[o]
if(t!=null)return t
s=v.interceptorsByTag[o]
if(s==null){r=A.b3($.eY.$2(a,o))
if(r!=null){n=$.dv[r]
if(n!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:n,enumerable:false,writable:true,configurable:true})
return n.i}t=$.dB[r]
if(t!=null)return t
s=v.interceptorsByTag[r]
o=r}}if(s==null)return null
t=s.prototype
q=o[0]
if(q==="!"){n=A.dE(t)
$.dv[o]=n
Object.defineProperty(a,v.dispatchPropertyName,{value:n,enumerable:false,writable:true,configurable:true})
return n.i}if(q==="~"){$.dB[o]=t
return t}if(q==="-"){p=A.dE(t)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}if(q==="+")return A.f1(a,t)
if(q==="*")throw A.a(A.ew(o))
if(v.leafTags[o]===true){p=A.dE(t)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}else return A.f1(a,t)},
f1(a,b){var t=Object.getPrototypeOf(a)
Object.defineProperty(t,v.dispatchPropertyName,{value:J.e6(b,t,null,null),enumerable:false,writable:true,configurable:true})
return b},
dE(a){return J.e6(a,!1,null,!!a.$iaW)},
ie(a,b,c){var t=b.prototype
if(v.leafTags[a]===true)return A.dE(t)
else return J.e6(t,c,null,null)},
i7(){if(!0===$.e4)return
$.e4=!0
A.i8()},
i8(){var t,s,r,q,p,o,n,m
$.dv=Object.create(null)
$.dB=Object.create(null)
A.i6()
t=v.interceptorsByTag
s=Object.getOwnPropertyNames(t)
if(typeof window!="undefined"){window
r=function(){}
for(q=0;q<s.length;++q){p=s[q]
o=$.f2.$1(p)
if(o!=null){n=A.ie(p,t[p],o)
if(n!=null){Object.defineProperty(o,v.dispatchPropertyName,{value:n,enumerable:false,writable:true,configurable:true})
r.prototype=o}}}}for(q=0;q<s.length;++q){p=s[q]
if(/^[A-Za-z_]/.test(p)){m=t[p]
t["!"+p]=m
t["~"+p]=m
t["-"+p]=m
t["+"+p]=m
t["*"+p]=m}}},
i6(){var t,s,r,q,p,o,n=B.R()
n=A.b6(B.S,A.b6(B.T,A.b6(B.I,A.b6(B.I,A.b6(B.U,A.b6(B.V,A.b6(B.W(B.H),n)))))))
if(typeof dartNativeDispatchHooksTransformer!="undefined"){t=dartNativeDispatchHooksTransformer
if(typeof t=="function")t=[t]
if(Array.isArray(t))for(s=0;s<t.length;++s){r=t[s]
if(typeof r=="function")n=r(n)||n}}q=n.getTag
p=n.getUnknownTag
o=n.prototypeForTag
$.f0=new A.dy(q)
$.eY=new A.dz(p)
$.f2=new A.dA(o)},
b6(a,b){return a(b)||b},
i_(a,b){var t=b.length,s=v.rttc[""+t+";"+a]
if(s==null)return null
if(t===0)return s
if(t===s.length)return s.apply(null,b)
return s(b)},
ih(a){if(/[[\]{}()*+?.\\^$|]/.test(a))return a.replace(/[[\]{}()*+?.\\^$|]/g,"\\$&")
return a},
r:function r(a,b){this.a=a
this.b=b},
b9:function b9(){},
av:function av(a,b,c){this.a=a
this.b=b
this.$ti=c},
bC:function bC(a,b){this.a=a
this.$ti=b},
ai:function ai(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
aP:function aP(){},
ba:function ba(a,b,c){this.a=a
this.b=b
this.$ti=c},
bc:function bc(a,b){this.a=a
this.$ti=b},
bt:function bt(){},
d_:function d_(a,b,c,d,e,f){var _=this
_.a=a
_.b=b
_.c=c
_.d=d
_.e=e
_.f=f},
bq:function bq(){},
c7:function c7(a,b,c){this.a=a
this.b=b
this.c=c},
cl:function cl(a){this.a=a},
cK:function cK(a){this.a=a},
ak:function ak(){},
bT:function bT(){},
cj:function cj(){},
ci:function ci(){},
aO:function aO(a,b){this.a=a
this.b=b},
cg:function cg(a){this.a=a},
aa:function aa(a){var _=this
_.a=0
_.f=_.e=_.d=_.c=_.b=null
_.r=0
_.$ti=a},
cH:function cH(a,b){this.a=a
this.b=b
this.c=null},
aA:function aA(a,b){this.a=a
this.$ti=b},
bi:function bi(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=null
_.$ti=d},
bg:function bg(a){var _=this
_.a=0
_.f=_.e=_.d=_.c=_.b=null
_.r=0
_.$ti=a},
dy:function dy(a){this.a=a},
dz:function dz(a){this.a=a},
dA:function dA(a){this.a=a},
ao:function ao(){},
b2:function b2(){},
dp(a,b,c){},
eL(a){return a},
fJ(a,b,c){var t
A.dp(a,b,c)
t=new DataView(a,b)
return t},
fK(a,b,c){var t
A.dp(a,b,c)
t=new Uint8Array(a,b)
return t},
dn(a,b,c){if(a>>>0!==a||a>=c)throw A.a(A.cw(b,a))},
hp(a,b,c){var t
if(!(a>>>0!==a))t=b>>>0!==b||a>b||b>c
else t=!0
if(t)throw A.a(A.i0(a,b,c))
return b},
aE:function aE(){},
bl:function bl(){},
d9:function d9(a){this.a=a},
cd:function cd(){},
a5:function a5(){},
ab:function ab(){},
bm:function bm(){},
bn:function bn(){},
bo:function bo(){},
bE:function bE(){},
bF:function bF(){},
dR(a,b){var t=b.c
return t==null?b.c=A.bJ(a,"ej",[b.x]):t},
es(a){var t=a.w
if(t===6||t===7)return A.es(a.x)
return t===11||t===12},
fQ(a){return a.as},
a_(a){return A.d8(v.typeUniverse,a,!1)},
aI(a0,a1,a2,a3){var t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b,a=a1.w
switch(a){case 5:case 1:case 2:case 3:case 4:return a1
case 6:t=a1.x
s=A.aI(a0,t,a2,a3)
if(s===t)return a1
return A.eE(a0,s,!0)
case 7:t=a1.x
s=A.aI(a0,t,a2,a3)
if(s===t)return a1
return A.eD(a0,s,!0)
case 8:r=a1.y
q=A.b5(a0,r,a2,a3)
if(q===r)return a1
return A.bJ(a0,a1.x,q)
case 9:p=a1.x
o=A.aI(a0,p,a2,a3)
n=a1.y
m=A.b5(a0,n,a2,a3)
if(o===p&&m===n)return a1
return A.dV(a0,o,m)
case 10:l=a1.x
k=a1.y
j=A.b5(a0,k,a2,a3)
if(j===k)return a1
return A.eF(a0,l,j)
case 11:i=a1.x
h=A.aI(a0,i,a2,a3)
g=a1.y
f=A.hQ(a0,g,a2,a3)
if(h===i&&f===g)return a1
return A.eC(a0,h,f)
case 12:e=a1.y
a3+=e.length
d=A.b5(a0,e,a2,a3)
p=a1.x
o=A.aI(a0,p,a2,a3)
if(d===e&&o===p)return a1
return A.dW(a0,o,d,!0)
case 13:c=a1.x
if(c<a3)return a1
b=a2[c-a3]
if(b==null)return a1
return b
default:throw A.a(A.bS("Attempted to substitute unexpected RTI kind "+a))}},
b5(a,b,c,d){var t,s,r,q,p=b.length,o=A.db(p)
for(t=!1,s=0;s<p;++s){r=b[s]
q=A.aI(a,r,c,d)
if(q!==r)t=!0
o[s]=q}return t?o:b},
hR(a,b,c,d){var t,s,r,q,p,o,n=b.length,m=A.db(n)
for(t=!1,s=0;s<n;s+=3){r=b[s]
q=b[s+1]
p=b[s+2]
o=A.aI(a,p,c,d)
if(o!==p)t=!0
m.splice(s,3,r,q,o)}return t?m:b},
hQ(a,b,c,d){var t,s=b.a,r=A.b5(a,s,c,d),q=b.b,p=A.b5(a,q,c,d),o=b.c,n=A.hR(a,o,c,d)
if(r===s&&p===q&&n===o)return b
t=new A.cp()
t.a=r
t.b=p
t.c=n
return t},
t(a,b){a[v.arrayRti]=b
return a},
eZ(a){var t=a.$S
if(t!=null){if(typeof t=="number")return A.i5(t)
return a.$S()}return null},
i9(a,b){var t
if(A.es(b))if(a instanceof A.ak){t=A.eZ(a)
if(t!=null)return t}return A.a0(a)},
a0(a){if(a instanceof A.m)return A.h(a)
if(Array.isArray(a))return A.P(a)
return A.dZ(J.ar(a))},
P(a){var t=a[v.arrayRti],s=u.b
if(t==null)return s
if(t.constructor!==s.constructor)return s
return t},
h(a){var t=a.$ti
return t!=null?t:A.dZ(a)},
dZ(a){var t=a.constructor,s=t.$ccache
if(s!=null)return s
return A.hy(a,t)},
hy(a,b){var t=a instanceof A.ak?Object.getPrototypeOf(Object.getPrototypeOf(a)).constructor:b,s=A.hb(v.typeUniverse,t.name)
b.$ccache=s
return s},
i5(a){var t,s=v.types,r=s[a]
if(typeof r=="string"){t=A.d8(v.typeUniverse,r,!1)
s[a]=t
return t}return r},
i4(a){return A.aJ(A.h(a))},
e0(a){var t
if(a instanceof A.ao)return A.i1(a.$r,a.aC())
t=a instanceof A.ak?A.eZ(a):null
if(t!=null)return t
if(u.l.b(a))return J.fr(a).a
if(Array.isArray(a))return A.P(a)
return A.a0(a)},
aJ(a){var t=a.r
return t==null?a.r=new A.cv(a):t},
i1(a,b){var t,s,r=b,q=r.length
if(q===0)return u.F
if(0>=q)return A.d(r,0)
t=A.bL(v.typeUniverse,A.e0(r[0]),"@<0>")
for(s=1;s<q;++s){if(!(s<r.length))return A.d(r,s)
t=A.eH(v.typeUniverse,t,A.e0(r[s]))}return A.bL(v.typeUniverse,t,a)},
bO(a){return A.aJ(A.d8(v.typeUniverse,a,!1))},
hx(a){var t=this
t.b=A.hP(t)
return t.b(a)},
hP(a){var t,s,r,q,p
if(a===u.K)return A.hG
if(A.aK(a))return A.hK
t=a.w
if(t===6)return A.hv
if(t===1)return A.eT
if(t===7)return A.hB
s=A.hO(a)
if(s!=null)return s
if(t===8){r=a.x
if(a.y.every(A.aK)){a.f="$i"+r
if(r==="n")return A.hE
if(a===u.m)return A.hD
return A.hJ}}else if(t===10){q=A.i_(a.x,a.y)
p=q==null?A.eT:q
return p==null?A.dX(p):p}return A.ht},
hO(a){if(a.w===8){if(a===u.S)return A.eR
if(a===u.i||a===u.H)return A.hF
if(a===u.N)return A.hI
if(a===u.y)return A.e_}return null},
hw(a){var t=this,s=A.hs
if(A.aK(t))s=A.hk
else if(t===u.K)s=A.dX
else if(A.b7(t)){s=A.hu
if(t===u.a3)s=A.eK
else if(t===u.aD)s=A.b3
else if(t===u.cG)s=A.hf
else if(t===u.n)s=A.aq
else if(t===u.dd)s=A.hh
else if(t===u.aQ)s=A.hj}else if(t===u.S)s=A.F
else if(t===u.N)s=A.L
else if(t===u.y)s=A.he
else if(t===u.H)s=A.j
else if(t===u.i)s=A.hg
else if(t===u.m)s=A.hi
t.a=s
return t.a(a)},
ht(a){var t=this
if(a==null)return A.b7(t)
return A.ib(v.typeUniverse,A.i9(a,t),t)},
hv(a){if(a==null)return!0
return this.x.b(a)},
hJ(a){var t,s=this
if(a==null)return A.b7(s)
t=s.f
if(a instanceof A.m)return!!a[t]
return!!J.ar(a)[t]},
hE(a){var t,s=this
if(a==null)return A.b7(s)
if(typeof a!="object")return!1
if(Array.isArray(a))return!0
t=s.f
if(a instanceof A.m)return!!a[t]
return!!J.ar(a)[t]},
hD(a){var t=this
if(a==null)return!1
if(typeof a=="object"){if(a instanceof A.m)return!!a[t.f]
return!0}if(typeof a=="function")return!0
return!1},
eS(a){if(typeof a=="object"){if(a instanceof A.m)return u.m.b(a)
return!0}if(typeof a=="function")return!0
return!1},
hs(a){var t=this
if(a==null){if(A.b7(t))return a}else if(t.b(a))return a
throw A.G(A.eM(a,t),new Error())},
hu(a){var t=this
if(a==null||t.b(a))return a
throw A.G(A.eM(a,t),new Error())},
eM(a,b){return new A.bH("TypeError: "+A.ex(a,A.S(b,null)))},
ex(a,b){return A.c_(a)+": type '"+A.S(A.e0(a),null)+"' is not a subtype of type '"+b+"'"},
W(a,b){return new A.bH("TypeError: "+A.ex(a,b))},
hB(a){var t=this
return t.x.b(a)||A.dR(v.typeUniverse,t).b(a)},
hG(a){return a!=null},
dX(a){if(a!=null)return a
throw A.G(A.W(a,"Object"),new Error())},
hK(a){return!0},
hk(a){return a},
eT(a){return!1},
e_(a){return!0===a||!1===a},
he(a){if(!0===a)return!0
if(!1===a)return!1
throw A.G(A.W(a,"bool"),new Error())},
hf(a){if(!0===a)return!0
if(!1===a)return!1
if(a==null)return a
throw A.G(A.W(a,"bool?"),new Error())},
hg(a){if(typeof a=="number")return a
throw A.G(A.W(a,"double"),new Error())},
hh(a){if(typeof a=="number")return a
if(a==null)return a
throw A.G(A.W(a,"double?"),new Error())},
eR(a){return typeof a=="number"&&Math.floor(a)===a},
F(a){if(typeof a=="number"&&Math.floor(a)===a)return a
throw A.G(A.W(a,"int"),new Error())},
eK(a){if(typeof a=="number"&&Math.floor(a)===a)return a
if(a==null)return a
throw A.G(A.W(a,"int?"),new Error())},
hF(a){return typeof a=="number"},
j(a){if(typeof a=="number")return a
throw A.G(A.W(a,"num"),new Error())},
aq(a){if(typeof a=="number")return a
if(a==null)return a
throw A.G(A.W(a,"num?"),new Error())},
hI(a){return typeof a=="string"},
L(a){if(typeof a=="string")return a
throw A.G(A.W(a,"String"),new Error())},
b3(a){if(typeof a=="string")return a
if(a==null)return a
throw A.G(A.W(a,"String?"),new Error())},
hi(a){if(A.eS(a))return a
throw A.G(A.W(a,"JSObject"),new Error())},
hj(a){if(a==null)return a
if(A.eS(a))return a
throw A.G(A.W(a,"JSObject?"),new Error())},
eW(a,b){var t,s,r
for(t="",s="",r=0;r<a.length;++r,s=", ")t+=s+A.S(a[r],b)
return t},
hN(a,b){var t,s,r,q,p,o,n=a.x,m=a.y
if(""===n)return"("+A.eW(m,b)+")"
t=m.length
s=n.split(",")
r=s.length-t
for(q="(",p="",o=0;o<t;++o,p=", "){q+=p
if(r===0)q+="{"
q+=A.S(m[o],b)
if(r>=0)q+=" "+s[r];++r}return q+"})"},
eO(a2,a3,a4){var t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b,a,a0=", ",a1=null
if(a4!=null){t=a4.length
if(a3==null)a3=A.t([],u.s)
else a1=a3.length
s=a3.length
for(r=t;r>0;--r)B.a.l(a3,"T"+(s+r))
for(q=u.X,p="<",o="",r=0;r<t;++r,o=a0){n=a3.length
m=n-1-r
if(!(m>=0))return A.d(a3,m)
p=p+o+a3[m]
l=a4[r]
k=l.w
if(!(k===2||k===3||k===4||k===5||l===q))p+=" extends "+A.S(l,a3)}p+=">"}else p=""
q=a2.x
j=a2.y
i=j.a
h=i.length
g=j.b
f=g.length
e=j.c
d=e.length
c=A.S(q,a3)
for(b="",a="",r=0;r<h;++r,a=a0)b+=a+A.S(i[r],a3)
if(f>0){b+=a+"["
for(a="",r=0;r<f;++r,a=a0)b+=a+A.S(g[r],a3)
b+="]"}if(d>0){b+=a+"{"
for(a="",r=0;r<d;r+=3,a=a0){b+=a
if(e[r+1])b+="required "
b+=A.S(e[r+2],a3)+" "+e[r]}b+="}"}if(a1!=null){a3.toString
a3.length=a1}return p+"("+b+") => "+c},
S(a,b){var t,s,r,q,p,o,n,m=a.w
if(m===5)return"erased"
if(m===2)return"dynamic"
if(m===3)return"void"
if(m===1)return"Never"
if(m===4)return"any"
if(m===6){t=a.x
s=A.S(t,b)
r=t.w
return(r===11||r===12?"("+s+")":s)+"?"}if(m===7)return"FutureOr<"+A.S(a.x,b)+">"
if(m===8){q=A.hS(a.x)
p=a.y
return p.length>0?q+("<"+A.eW(p,b)+">"):q}if(m===10)return A.hN(a,b)
if(m===11)return A.eO(a,b,null)
if(m===12)return A.eO(a.x,b,a.y)
if(m===13){o=a.x
n=b.length
o=n-1-o
if(!(o>=0&&o<n))return A.d(b,o)
return b[o]}return"?"},
hS(a){var t=A.f3(a)
if(t!=null)return t
return"minified:"+a},
hc(a,b){var t=a.tR[b]
while(typeof t=="string")t=a.tR[t]
return t},
hb(a,b){var t,s,r,q,p,o=a.eT,n=o[b]
if(n==null)return A.d8(a,b,!1)
else if(typeof n=="number"){t=n
s=A.bK(a,5,"#")
r=A.db(t)
for(q=0;q<t;++q)r[q]=s
p=A.bJ(a,b,r)
o[b]=p
return p}else return n},
ha(a,b){return A.eI(a.tR,b)},
h9(a,b){return A.eI(a.eT,b)},
d8(a,b,c){var t,s=a.eC,r=s.get(b)
if(r!=null)return r
t=A.eG(a,null,b,!1)
s.set(b,t)
return t},
bL(a,b,c){var t,s,r=b.z
if(r==null)r=b.z=new Map()
t=r.get(c)
if(t!=null)return t
s=A.eG(a,b,c,!0)
r.set(c,s)
return s},
eH(a,b,c){var t,s,r,q=b.Q
if(q==null)q=b.Q=new Map()
t=c.as
s=q.get(t)
if(s!=null)return s
r=A.dV(a,b,c.w===9?c.y:[c])
q.set(t,r)
return r},
eG(a,b,c,d){return A.h2(A.fX(a,b,c,d))},
ap(a,b){b.a=A.hw
b.b=A.hx
return b},
bK(a,b,c){var t,s,r=a.eC.get(c)
if(r!=null)return r
t=new A.Z(null,null)
t.w=b
t.as=c
s=A.ap(a,t)
a.eC.set(c,s)
return s},
eE(a,b,c){var t,s=b.as+"?",r=a.eC.get(s)
if(r!=null)return r
t=A.h7(a,b,s,c)
a.eC.set(s,t)
return t},
h7(a,b,c,d){var t,s,r
if(d){t=b.w
s=!0
if(!A.aK(b))if(!(b===u.a||b===u.T))if(t!==6)s=t===7&&A.b7(b.x)
if(s)return b
else if(t===1)return u.a}r=new A.Z(null,null)
r.w=6
r.x=b
r.as=c
return A.ap(a,r)},
eD(a,b,c){var t,s=b.as+"/",r=a.eC.get(s)
if(r!=null)return r
t=A.h5(a,b,s,c)
a.eC.set(s,t)
return t},
h5(a,b,c,d){var t,s
if(d){t=b.w
if(A.aK(b)||b===u.K)return b
else if(t===1)return A.bJ(a,"ej",[b])
else if(b===u.a||b===u.T)return u.bc}s=new A.Z(null,null)
s.w=7
s.x=b
s.as=c
return A.ap(a,s)},
h8(a,b){var t,s,r=""+b+"^",q=a.eC.get(r)
if(q!=null)return q
t=new A.Z(null,null)
t.w=13
t.x=b
t.as=r
s=A.ap(a,t)
a.eC.set(r,s)
return s},
bI(a){var t,s,r,q=a.length
for(t="",s="",r=0;r<q;++r,s=",")t+=s+a[r].as
return t},
h4(a){var t,s,r,q,p,o=a.length
for(t="",s="",r=0;r<o;r+=3,s=","){q=a[r]
p=a[r+1]?"!":":"
t+=s+q+p+a[r+2].as}return t},
bJ(a,b,c){var t,s,r,q=b
if(c.length>0)q+="<"+A.bI(c)+">"
t=a.eC.get(q)
if(t!=null)return t
s=new A.Z(null,null)
s.w=8
s.x=b
s.y=c
if(c.length>0)s.c=c[0]
s.as=q
r=A.ap(a,s)
a.eC.set(q,r)
return r},
dV(a,b,c){var t,s,r,q,p,o
if(b.w===9){t=b.x
s=b.y.concat(c)}else{s=c
t=b}r=t.as+(";<"+A.bI(s)+">")
q=a.eC.get(r)
if(q!=null)return q
p=new A.Z(null,null)
p.w=9
p.x=t
p.y=s
p.as=r
o=A.ap(a,p)
a.eC.set(r,o)
return o},
eF(a,b,c){var t,s,r="+"+(b+"("+A.bI(c)+")"),q=a.eC.get(r)
if(q!=null)return q
t=new A.Z(null,null)
t.w=10
t.x=b
t.y=c
t.as=r
s=A.ap(a,t)
a.eC.set(r,s)
return s},
eC(a,b,c){var t,s,r,q,p,o=b.as,n=c.a,m=n.length,l=c.b,k=l.length,j=c.c,i=j.length,h="("+A.bI(n)
if(k>0){t=m>0?",":""
h+=t+"["+A.bI(l)+"]"}if(i>0){t=m>0?",":""
h+=t+"{"+A.h4(j)+"}"}s=o+(h+")")
r=a.eC.get(s)
if(r!=null)return r
q=new A.Z(null,null)
q.w=11
q.x=b
q.y=c
q.as=s
p=A.ap(a,q)
a.eC.set(s,p)
return p},
dW(a,b,c,d){var t,s=b.as+("<"+A.bI(c)+">"),r=a.eC.get(s)
if(r!=null)return r
t=A.h6(a,b,c,s,d)
a.eC.set(s,t)
return t},
h6(a,b,c,d,e){var t,s,r,q,p,o,n,m
if(e){t=c.length
s=A.db(t)
for(r=0,q=0;q<t;++q){p=c[q]
if(p.w===1){s[q]=p;++r}}if(r>0){o=A.aI(a,b,s,0)
n=A.b5(a,c,s,0)
return A.dW(a,o,n,c!==n)}}m=new A.Z(null,null)
m.w=12
m.x=b
m.y=c
m.as=d
return A.ap(a,m)},
fX(a,b,c,d){return{u:a,e:b,r:c,s:[],p:0,n:d}},
h2(a){var t,s,r,q,p,o,n,m=a.r,l=a.s
for(t=m.length,s=0;s<t;){r=m.charCodeAt(s)
if(r>=48&&r<=57)s=A.fZ(s+1,r,m,l)
else if((((r|32)>>>0)-97&65535)<26||r===95||r===36||r===124)s=A.eA(a,s,m,l,!1)
else if(r===46)s=A.eA(a,s,m,l,!0)
else{++s
switch(r){case 44:break
case 58:l.push(!1)
break
case 33:l.push(!0)
break
case 59:l.push(A.aH(a.u,a.e,l.pop()))
break
case 94:l.push(A.h8(a.u,l.pop()))
break
case 35:l.push(A.bK(a.u,5,"#"))
break
case 64:l.push(A.bK(a.u,2,"@"))
break
case 126:l.push(A.bK(a.u,3,"~"))
break
case 60:l.push(a.p)
a.p=l.length
break
case 62:A.h0(a,l)
break
case 38:A.h_(a,l)
break
case 63:q=a.u
l.push(A.eE(q,A.aH(q,a.e,l.pop()),a.n))
break
case 47:q=a.u
l.push(A.eD(q,A.aH(q,a.e,l.pop()),a.n))
break
case 40:l.push(-3)
l.push(a.p)
a.p=l.length
break
case 41:A.fY(a,l)
break
case 91:l.push(a.p)
a.p=l.length
break
case 93:p=l.splice(a.p)
A.eB(a.u,a.e,p)
a.p=l.pop()
l.push(p)
l.push(-1)
break
case 123:l.push(a.p)
a.p=l.length
break
case 125:p=l.splice(a.p)
A.h3(a.u,a.e,p)
a.p=l.pop()
l.push(p)
l.push(-2)
break
case 43:o=m.indexOf("(",s)
l.push(m.substring(s,o))
l.push(-4)
l.push(a.p)
a.p=l.length
s=o+1
break
default:throw"Bad character "+r}}}n=l.pop()
return A.aH(a.u,a.e,n)},
fZ(a,b,c,d){var t,s,r=b-48
for(t=c.length;a<t;++a){s=c.charCodeAt(a)
if(!(s>=48&&s<=57))break
r=r*10+(s-48)}d.push(r)
return a},
eA(a,b,c,d,e){var t,s,r,q,p,o,n=b+1
for(t=c.length;n<t;++n){s=c.charCodeAt(n)
if(s===46){if(e)break
e=!0}else{if(!((((s|32)>>>0)-97&65535)<26||s===95||s===36||s===124))r=s>=48&&s<=57
else r=!0
if(!r)break}}q=c.substring(b,n)
if(e){t=a.u
p=a.e
if(p.w===9)p=p.x
o=A.hc(t,p.x)[q]
if(o==null)A.i('No "'+q+'" in "'+A.fQ(p)+'"')
d.push(A.bL(t,p,o))}else d.push(q)
return n},
h0(a,b){var t,s=a.u,r=A.ez(a,b),q=b.pop()
if(typeof q=="string")b.push(A.bJ(s,q,r))
else{t=A.aH(s,a.e,q)
switch(t.w){case 11:b.push(A.dW(s,t,r,a.n))
break
default:b.push(A.dV(s,t,r))
break}}},
fY(a,b){var t,s,r,q=a.u,p=b.pop(),o=null,n=null
if(typeof p=="number")switch(p){case-1:o=b.pop()
break
case-2:n=b.pop()
break
default:b.push(p)
break}else b.push(p)
t=A.ez(a,b)
p=b.pop()
switch(p){case-3:p=b.pop()
if(o==null)o=q.sEA
if(n==null)n=q.sEA
s=A.aH(q,a.e,p)
r=new A.cp()
r.a=t
r.b=o
r.c=n
b.push(A.eC(q,s,r))
return
case-4:b.push(A.eF(q,b.pop(),t))
return
default:throw A.a(A.bS("Unexpected state under `()`: "+A.l(p)))}},
h_(a,b){var t=b.pop()
if(0===t){b.push(A.bK(a.u,1,"0&"))
return}if(1===t){b.push(A.bK(a.u,4,"1&"))
return}throw A.a(A.bS("Unexpected extended operation "+A.l(t)))},
ez(a,b){var t=b.splice(a.p)
A.eB(a.u,a.e,t)
a.p=b.pop()
return t},
aH(a,b,c){if(typeof c=="string")return A.bJ(a,c,a.sEA)
else if(typeof c=="number"){b.toString
return A.h1(a,b,c)}else return c},
eB(a,b,c){var t,s=c.length
for(t=0;t<s;++t)c[t]=A.aH(a,b,c[t])},
h3(a,b,c){var t,s=c.length
for(t=2;t<s;t+=3)c[t]=A.aH(a,b,c[t])},
h1(a,b,c){var t,s,r=b.w
if(r===9){if(c===0)return b.x
t=b.y
s=t.length
if(c<=s)return t[c-1]
c-=s
b=b.x
r=b.w}else if(c===0)return b
if(r!==8)throw A.a(A.bS("Indexed base must be an interface type"))
t=b.y
if(c<=t.length)return t[c-1]
throw A.a(A.bS("Bad index "+c+" for "+b.k(0)))},
ib(a,b,c){var t,s=b.d
if(s==null)s=b.d=new Map()
t=s.get(c)
if(t==null){t=A.B(a,b,null,c,null)
s.set(c,t)}return t},
B(a,b,c,d,e){var t,s,r,q,p,o,n,m,l,k,j
if(b===d)return!0
if(A.aK(d))return!0
t=b.w
if(t===4)return!0
if(A.aK(b))return!1
if(b.w===1)return!0
s=t===13
if(s)if(A.B(a,c[b.x],c,d,e))return!0
r=d.w
q=u.a
if(b===q||b===u.T){if(r===7)return A.B(a,b,c,d.x,e)
return d===q||d===u.T||r===6}if(d===u.K){if(t===7)return A.B(a,b.x,c,d,e)
return t!==6}if(t===7){if(!A.B(a,b.x,c,d,e))return!1
return A.B(a,A.dR(a,b),c,d,e)}if(t===6)return A.B(a,q,c,d,e)&&A.B(a,b.x,c,d,e)
if(r===7){if(A.B(a,b,c,d.x,e))return!0
return A.B(a,b,c,A.dR(a,d),e)}if(r===6)return A.B(a,b,c,q,e)||A.B(a,b,c,d.x,e)
if(s)return!1
q=t!==11
if((!q||t===12)&&d===u.Z)return!0
p=t===10
if(p&&d===u.J)return!0
if(r===12){if(b===u.M)return!0
if(t!==12)return!1
o=b.y
n=d.y
m=o.length
if(m!==n.length)return!1
c=c==null?o:o.concat(c)
e=e==null?n:n.concat(e)
for(l=0;l<m;++l){k=o[l]
j=n[l]
if(!A.B(a,k,c,j,e)||!A.B(a,j,e,k,c))return!1}return A.eQ(a,b.x,c,d.x,e)}if(r===11){if(b===u.M)return!0
if(q)return!1
return A.eQ(a,b,c,d,e)}if(t===8){if(r!==8)return!1
return A.hC(a,b,c,d,e)}if(p&&r===10)return A.hH(a,b,c,d,e)
return!1},
eQ(a2,a3,a4,a5,a6){var t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b,a,a0,a1
if(!A.B(a2,a3.x,a4,a5.x,a6))return!1
t=a3.y
s=a5.y
r=t.a
q=s.a
p=r.length
o=q.length
if(p>o)return!1
n=o-p
m=t.b
l=s.b
k=m.length
j=l.length
if(p+k<o+j)return!1
for(i=0;i<p;++i){h=r[i]
if(!A.B(a2,q[i],a6,h,a4))return!1}for(i=0;i<n;++i){h=m[i]
if(!A.B(a2,q[p+i],a6,h,a4))return!1}for(i=0;i<j;++i){h=m[n+i]
if(!A.B(a2,l[i],a6,h,a4))return!1}g=t.c
f=s.c
e=g.length
d=f.length
for(c=0,b=0;b<d;b+=3){a=f[b]
for(;;){if(c>=e)return!1
a0=g[c]
c+=3
if(a<a0)return!1
a1=g[c-2]
if(a0<a){if(a1)return!1
continue}h=f[b+1]
if(a1&&!h)return!1
h=g[c-1]
if(!A.B(a2,f[b+2],a6,h,a4))return!1
break}}while(c<e){if(g[c+1])return!1
c+=3}return!0},
hC(a,b,c,d,e){var t,s,r,q,p,o=b.x,n=d.x
while(o!==n){t=a.tR[o]
if(t==null)return!1
if(typeof t=="string"){o=t
continue}s=t[n]
if(s==null)return!1
r=s.length
q=r>0?new Array(r):v.typeUniverse.sEA
for(p=0;p<r;++p)q[p]=A.bL(a,b,s[p])
return A.eJ(a,q,null,c,d.y,e)}return A.eJ(a,b.y,null,c,d.y,e)},
eJ(a,b,c,d,e,f){var t,s=b.length
for(t=0;t<s;++t)if(!A.B(a,b[t],d,e[t],f))return!1
return!0},
hH(a,b,c,d,e){var t,s=b.y,r=d.y,q=s.length
if(q!==r.length)return!1
if(b.x!==d.x)return!1
for(t=0;t<q;++t)if(!A.B(a,s[t],c,r[t],e))return!1
return!0},
b7(a){var t=a.w,s=!0
if(!(a===u.a||a===u.T))if(!A.aK(a))if(t!==6)s=t===7&&A.b7(a.x)
return s},
aK(a){var t=a.w
return t===2||t===3||t===4||t===5||a===u.X},
eI(a,b){var t,s,r=Object.keys(b),q=r.length
for(t=0;t<q;++t){s=r[t]
a[s]=b[s]}},
db(a){return a>0?new Array(a):v.typeUniverse.sEA},
Z:function Z(a,b){var _=this
_.a=a
_.b=b
_.r=_.f=_.d=_.c=null
_.w=0
_.as=_.Q=_.z=_.y=_.x=null},
cp:function cp(){this.c=this.b=this.a=null},
cv:function cv(a){this.a=a},
co:function co(){},
bH:function bH(a){this.a=a},
w(a,b,c){return b.i("@<0>").q(c).i("dO<1,2>").a(A.i2(a,new A.aa(b.i("@<0>").q(c).i("aa<1,2>"))))},
dP(a,b){return new A.aa(a.i("@<0>").q(b).i("aa<1,2>"))},
cc(a){return new A.aF(a.i("aF<0>"))},
dU(){var t=Object.create(null)
t["<non-identifier-key>"]=t
delete t["<non-identifier-key>"]
return t},
ey(a,b,c){var t=new A.aG(a,b,c.i("aG<0>"))
t.c=a.e
return t},
en(a,b){var t,s,r=A.cc(b)
for(t=a.length,s=0;s<a.length;a.length===t||(0,A.aM)(a),++s)r.l(0,b.a(a[s]))
return r},
eo(a,b){var t=A.cc(b)
t.O(0,a)
return t},
dQ(a){var t,s
if(A.e5(a))return"{...}"
t=new A.b_("")
try{s={}
B.a.l($.T,a)
t.a+="{"
s.a=!0
a.N(0,new A.cJ(s,t))
t.a+="}"}finally{if(0>=$.T.length)return A.d($.T,-1)
$.T.pop()}s=t.a
return s.charCodeAt(0)==0?s:s},
fG(a){return 8},
aF:function aF(a){var _=this
_.a=0
_.f=_.e=_.d=_.c=_.b=null
_.r=0
_.$ti=a},
cs:function cs(a){this.a=a
this.c=this.b=null},
aG:function aG(a,b,c){var _=this
_.a=a
_.b=b
_.d=_.c=null
_.$ti=c},
x:function x(){},
z:function z(){},
cJ:function cJ(a,b){this.a=a
this.b=b},
bj:function bj(a,b){var _=this
_.a=a
_.d=_.c=_.b=0
_.$ti=b},
bD:function bD(a,b,c,d,e){var _=this
_.a=a
_.b=b
_.c=c
_.d=d
_.e=null
_.$ti=e},
ad:function ad(){},
bG:function bG(){},
hM(a,b){var t,s,r,q=null
try{q=JSON.parse(a)}catch(s){t=A.e8(s)
r=String(t)
throw A.a(new A.cE(r))}r=A.dq(q)
return r},
dq(a){var t
if(a==null)return null
if(typeof a!="object")return a
if(!Array.isArray(a))return new A.cq(a,Object.create(null))
for(t=0;t<a.length;++t)a[t]=A.dq(a[t])
return a},
em(a,b,c){return new A.bh(a,b)},
hq(a){return a.bH()},
fV(a,b){return new A.d4(a,[],A.hZ())},
fW(a,b,c){var t,s=new A.b_(""),r=A.fV(s,b)
r.a7(a)
t=s.a
return t.charCodeAt(0)==0?t:t},
cq:function cq(a,b){this.a=a
this.b=b
this.c=null},
cr:function cr(a){this.a=a},
bU:function bU(){},
aQ:function aQ(){},
bh:function bh(a,b){this.a=a
this.b=b},
c9:function c9(a,b){this.a=a
this.b=b},
c8:function c8(){},
cb:function cb(a){this.b=a},
ca:function ca(a){this.a=a},
d5:function d5(){},
d6:function d6(a,b){this.a=a
this.b=b},
d4:function d4(a,b,c){this.c=a
this.a=b
this.b=c},
cm:function cm(){},
da:function da(a){this.b=0
this.c=a},
cI(a,b,c,d){var t,s=J.el(a,d)
if(a!==0&&b!=null)for(t=0;t<a;++t)s[t]=b
return s},
fH(a,b,c){var t,s,r=A.t([],c.i("o<0>"))
for(t=a.length,s=0;s<a.length;a.length===t||(0,A.aM)(a),++s)B.a.l(r,c.a(a[s]))
r.$flags=1
return r},
aC(a,b){var t,s
if(Array.isArray(a))return A.t(a.slice(0),b.i("o<0>"))
t=A.t([],b.i("o<0>"))
for(s=J.cy(a);s.m();)B.a.l(t,s.gn())
return t},
fS(a){var t
A.V(0,"start")
t=A.fT(a,0,null)
return t},
fT(a,b,c){var t=a.length
if(b>=t)return""
return A.fN(a,b,t)},
eu(a,b,c){var t=J.cy(b)
if(!t.m())return a
if(c.length===0){do a+=A.l(t.gn())
while(t.m())}else{a+=A.l(t.gn())
while(t.m())a=a+c+A.l(t.gn())}return a},
cD(a,b,c){var t,s,r
for(t=a.length,s=0;s<t;++s){r=a[s]
if(r.b===b)return r}throw A.a(A.fs(b,"name","No enum value with that name"))},
c_(a){if(typeof a=="number"||A.e_(a)||a==null)return J.aj(a)
if(typeof a=="string")return JSON.stringify(a)
return A.er(a)},
bS(a){return new A.bR(a)},
X(a){return new A.a3(!1,null,null,a)},
fs(a,b,c){return new A.a3(!0,a,b,c)},
cz(a,b,c){return a},
fP(a,b){return new A.bs(null,null,!0,a,b,"Value not in range")},
a6(a,b,c,d,e){return new A.bs(b,c,!0,a,d,"Invalid value")},
cM(a,b,c){if(0>a||a>c)throw A.a(A.a6(a,0,c,"start",null))
if(b!=null){if(a>b||b>c)throw A.a(A.a6(b,a,c,"end",null))
return b}return c},
V(a,b){if(a<0)throw A.a(A.a6(a,0,null,b,null))
return a},
c2(a,b,c,d,e){return new A.c1(b,!0,a,e,"Index out of range")},
b1(a){return new A.bz(a)},
ew(a){return new A.ck(a)},
af(a){return new A.aZ(a)},
N(a){return new A.bV(a)},
fB(a,b,c){var t,s
if(A.e5(a)){if(b==="("&&c===")")return"(...)"
return b+"..."+c}t=A.t([],u.s)
B.a.l($.T,a)
try{A.hL(a,t)}finally{if(0>=$.T.length)return A.d($.T,-1)
$.T.pop()}s=A.eu(b,u.U.a(t),", ")+c
return s.charCodeAt(0)==0?s:s},
cF(a,b,c){var t,s
if(A.e5(a))return b+"..."+c
t=new A.b_(b)
B.a.l($.T,a)
try{s=t
s.a=A.eu(s.a,a,", ")}finally{if(0>=$.T.length)return A.d($.T,-1)
$.T.pop()}t.a+=c
s=t.a
return s.charCodeAt(0)==0?s:s},
hL(a,b){var t,s,r,q,p,o,n,m=a.gp(a),l=0,k=0
for(;;){if(!(l<80||k<3))break
if(!m.m())return
t=A.l(m.gn())
B.a.l(b,t)
l+=t.length+2;++k}if(!m.m()){if(k<=5)return
if(0>=b.length)return A.d(b,-1)
s=b.pop()
if(0>=b.length)return A.d(b,-1)
r=b.pop()}else{q=m.gn();++k
if(!m.m()){if(k<=4){B.a.l(b,A.l(q))
return}s=A.l(q)
if(0>=b.length)return A.d(b,-1)
r=b.pop()
l+=s.length+2}else{p=m.gn();++k
for(;m.m();q=p,p=o){o=m.gn();++k
if(k>100){for(;;){if(!(l>75&&k>3))break
if(0>=b.length)return A.d(b,-1)
l-=b.pop().length+2;--k}B.a.l(b,"...")
return}}r=A.l(q)
s=A.l(p)
l+=s.length+r.length+4}}if(k>b.length+2){l+=5
n="..."}else n=null
for(;;){if(!(l>80&&b.length>3))break
if(0>=b.length)return A.d(b,-1)
l-=b.pop().length+2
if(n==null){l+=5
n="..."}}if(n!=null)B.a.l(b,n)
B.a.l(b,r)
B.a.l(b,s)},
ep(a,b,c,d,e){return new A.au(a,b.i("@<0>").q(c).q(d).q(e).i("au<1,2,3,4>"))},
fL(a,b,c,d){var t
if(B.r===c){t=B.f.gv(a)
b=J.a2(b)
return A.cZ(A.ag(A.ag($.cx(),t),b))}if(B.r===d){t=B.f.gv(a)
b=J.a2(b)
c=J.a2(c)
return A.cZ(A.ag(A.ag(A.ag($.cx(),t),b),c))}t=B.f.gv(a)
b=J.a2(b)
c=J.a2(c)
d=J.a2(d)
d=A.cZ(A.ag(A.ag(A.ag(A.ag($.cx(),t),b),c),d))
return d},
fM(a){var t,s,r=$.cx()
for(t=a.length,s=0;s<a.length;a.length===t||(0,A.aM)(a),++s)r=A.ag(r,J.a2(a[s]))
return A.cZ(r)},
cn:function cn(){},
u:function u(){},
bR:function bR(a){this.a=a},
by:function by(){},
a3:function a3(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
bs:function bs(a,b,c,d,e,f){var _=this
_.e=a
_.f=b
_.a=c
_.b=d
_.c=e
_.d=f},
c1:function c1(a,b,c,d,e){var _=this
_.f=a
_.a=b
_.b=c
_.c=d
_.d=e},
bz:function bz(a){this.a=a},
ck:function ck(a){this.a=a},
aZ:function aZ(a){this.a=a},
bV:function bV(a){this.a=a},
bw:function bw(){},
d2:function d2(a){this.a=a},
cE:function cE(a){this.a=a},
b:function b(){},
bp:function bp(){},
m:function m(){},
b_:function b_(a){this.a=a},
bY:function bY(){},
eP(a){var t,s,r,q,p="0123456789abcdef",o=a.length,n=o*2,m=new Uint8Array(n)
for(t=0,s=0;t<o;++t){r=a[t]
q=s+1
if(!(s<n))return A.d(m,s)
m[s]=p.charCodeAt(r>>>4&15)
s=q+1
if(!(q<n))return A.d(m,q)
m[q]=p.charCodeAt(r&15)}return A.fS(m)},
aR:function aR(a){this.a=a},
bW:function bW(){this.a=null},
c0:function c0(){},
cu:function cu(){},
ct:function ct(a,b,c,d,e){var _=this
_.y=a
_.z=b
_.a=c
_.c=null
_.d=d
_.e=0
_.f=e
_.r=0
_.w=!1},
io(a){return a.aO(0,B.h,new A.dH(),u.R)},
p:function p(a,b){this.a=a
this.b=b},
dH:function dH(){},
O:function O(a,b){this.a=a
this.b=b},
a4:function a4(a,b){this.a=a
this.b=b},
Y:function Y(a,b){this.a=a
this.b=b},
bX:function bX(a,b){var _=this
_.a=a
_.c=b
_.f=_.e=_.d=$},
dr(a,b,c,d,e){var t=e==null?B.d:e
return new A.cB(c,d,a.b,t)},
dY(a,b,c){var t,s=b.H(0).bq(J.eb(c,new A.dm(),u.N).H(0))
if(s.a!==0){t=s.a6(0)
B.a.a8(t)
throw A.a(A.X("unknown "+a+": "+A.l(t)))}},
hl(a,b){return u.f.a(J.fn(a,new A.dl(b)))},
ig(c2,c3,c4,c5,c6){var t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b,a,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,b0="emergency_symptoms",b1="red_symptoms",b2="yellow_symptoms",b3="red_conditions",b4="yellow_conditions",b5="pre_check",b6="source_grades",b7="systolic",b8="diastolic",b9="plausibility",c0=c2.a,c1=c0.a
c0=c0.$ti.i("4?")
t=c0.a(c1.h(0,"precheck"))
s=c6.H(c6)
r=c5.H(c5)
q=J.A(t)
p=u.U
o=u.z
n=A.aC(p.a(q.h(t,b0)),o)
B.a.O(n,p.a(q.h(t,b1)))
B.a.O(n,p.a(q.h(t,b2)))
A.dY("symptom",s,n)
n=A.aC(p.a(q.h(t,b3)),o)
B.a.O(n,p.a(q.h(t,b4)))
A.dY("condition",r,n)
n=u.j
m=u.N
l=J.bP(n.a(q.h(t,b0)),m)
l=s.ak(l.H(l))
k=A.aC(l,A.h(l).c)
B.a.a8(k)
if(k.length!==0)return A.dr(c2,b5,"EMERGENCY",A.t(["PRE_EMERGENCY_SYMPTOM"],u.s),A.w(["symptoms",k],m,o))
j=c0.a(c1.h(0,"hard_gate"))
o=c3.b
l=J.A(j)
A.dY("gate condition",o,p.a(l.h(j,"conditions_requiring_clearance")))
p=u.s
i=A.t([],p)
if(!c3.d){if(o.a!==0)B.a.l(i,"GATE_CONDITION_NEEDS_CLEARANCE")
if(c3.c&&J.v(l.h(j,"parq_risk_requires_clearance"),!0))B.a.l(i,"GATE_PARQ_RISK")}if(J.bQ(n.a(l.h(j,"devices_requiring_doctor_hr_ceiling")),c3.f)&&c3.r.d==null)B.a.l(i,"GATE_DEVICE_NEEDS_HR_CEILING")
if(i.length!==0)return A.dr(c2,b5,"BLOCKED",i,null)
h=A.t([],u.e)
g=new A.dF(t)
if(g.$2(s,b1))B.a.l(h,B.aE)
if(g.$2(s,b2))B.a.l(h,B.ay)
if(g.$2(r,b3))B.a.l(h,B.aD)
if(g.$2(r,b4))B.a.l(h,B.ax)
o=c4.d
f=J.f(J.f(c0.a(c1.h(0,b6)),"blood_pressure"),o)
l=c4.e
e=J.f(J.f(c0.a(c1.h(0,b6)),"heart_rate"),l)
if(f==null||e==null)throw A.a(A.X("unknown measurement source: bp="+o+" hr="+l))
o=!J.v(f,"A")
if(o)B.a.l(h,B.az)
d=A.w(["systolic",c4.a,"diastolic",c4.b,"resting_hr",c4.c],m,u.n)
c=A.dP(m,u.H)
for(m=c3.r,l=u.R,b=J.ar(e),a=0;a<3;++a){a0=B.ah[a]
a1=a0==="resting_hr"
if(!a1&&o)continue
a2=d.h(0,a0)
if(a2==null){B.a.l(h,B.aB)
continue}a3=J.f(c0.a(c1.h(0,b9)),a0)
a4=J.A(a3)
a5=a4.h(a3,"min")
if(typeof a5!=="number")return a5.S()
if(!(a5<=a2&&a2<=A.j(a4.h(a3,"max")))){B.a.l(h,B.O)
continue}c.A(0,a0,a2)
a6=A.hl(n.a(J.f(q.h(t,"bands"),a0)),a2)
a4=A.cD(B.w,A.L(a6.h(0,"light")),l)
if(a1&&b.R(e,"B")&&a4===B.h)B.a.l(h,B.aA)
else B.a.l(h,new A.r(a4,A.L(a6.h(0,"code"))))
a1=B.ai.h(0,a0)
a1.toString
a7=m.bk(a1)
a8=A.j(J.f(q.h(t,"doctor_limit_defaults"),a1))
if(a7!=null)if(a7>a8)B.a.l(h,B.aw)
else if(a2>=a7)B.a.l(h,B.aC)}q=!1
if(J.v(J.f(c0.a(c1.h(0,b9)),"require_systolic_above_diastolic"),!0))if(c.C(b7))if(c.C(b8)){c0=c.h(0,b7)
c0.toString
c1=c.h(0,b8)
c1.toString
c1=c0<=c1
c0=c1}else c0=q
else c0=q
else c0=q
if(c0)B.a.l(h,B.O)
a9=A.io(new A.R(h,u.r.a(new A.dG()),u.B))
i=A.t([],p)
for(c0=h.length,a=0;a<h.length;h.length===c0||(0,A.aM)(h),++a){c1=h[a].b
if(!B.a.B(i,c1))B.a.l(i,c1)}return A.dr(c2,b5,a9.b,i,null)},
hU(a,b,c){var t,s,r="hr_ceiling_pct_cap"
if(b!==B.h&&b!==B.n)return A.w(["allowed",!1,"max_minutes",0],u.N,u.z)
t=a.a
s=J.f(t.$ti.i("4?").a(t.a.h(0,"allowance")),b.b)
t=J.A(s)
return A.w(["allowed",!0,"max_minutes",Math.min(c,Math.max(A.F(t.h(s,"min_minutes")),B.c.aN(c*A.j(t.h(s,"minutes_factor"))))),"intensity",t.h(s,"intensity"),r,t.h(s,r)],u.N,u.z)},
cC:function cC(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
cL:function cL(a,b,c,d,e,f,g){var _=this
_.a=a
_.b=b
_.c=c
_.d=d
_.e=e
_.f=f
_.r=g},
d1:function d1(a,b,c,d,e){var _=this
_.a=a
_.b=b
_.c=c
_.d=d
_.e=e},
cB:function cB(a,b,c,d){var _=this
_.b=a
_.c=b
_.d=c
_.f=d},
dm:function dm(){},
dl:function dl(a){this.a=a},
dF:function dF(a){this.a=a},
dG:function dG(){},
y(a){return new A.cO(a)},
e1(a){var t,s
if(u.f.b(a)){t=a.gK().U(0,new A.dt(),u.N).a6(0)
B.a.a8(t)
s=A.P(t)
return"{"+new A.R(t,s.i("c(1)").a(new A.du(a)),s.i("R<1,c>")).aP(0,",")+"}"}if(u.j.b(a))return"["+J.eb(a,A.ii(),u.N).aP(0,",")+"]"
if(typeof a=="number")s=a===(a<0?Math.ceil(a):Math.floor(a))&&isFinite(a)
else s=!1
if(s)return""+B.c.aQ(a)+".0"
return B.b.D(a,null)},
ho(a,b){var t,s,r,q,p,o,n,m,l,k,j="lower",i="upper",h=J.U(b)
if(!h.gJ(b))A.i(A.y(a+": no bands"))
if(J.f(h.gE(b),j)!=null)A.i(A.y(a+": first band must start at null (-inf)"))
if(J.f(h.gF(b),i)!=null)A.i(A.y(a+": last band must end at null (+inf)"))
for(t=a+": gap or overlap between ",s=1;s<h.gj(b);++s){r=h.h(b,s-1)
q=h.h(b,s)
p=J.A(r)
p=p.h(r,i)!=null&&J.v(p.h(r,i),J.f(q,j))
o=A.l(r)
n=A.l(q)
if(!p)A.i(A.y(t+o+" and "+n))}for(h=h.gp(b),t=a+": band without code",p=a+": bad light ",o=a+": empty band ";h.m();){m=h.gn()
n=J.A(m)
l=B.aG.B(0,n.h(m,"light"))
k=A.l(n.h(m,"light"))
if(!l)A.i(A.y(p+k))
l=n.h(m,"code")
if(J.v(l==null?"":l,""))A.i(A.y(t))
if(n.h(m,j)!=null&&n.h(m,i)!=null){l=A.j(n.h(m,j))
n=A.j(n.h(m,i))
k=A.l(m)
if(!(l<n))A.i(A.y(o+k))}}},
im(a3){var t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c="meta",b="allowance",a="initial",a0="escalated",a1="absolute_max",a2="zone_pct"
for(t=["meta","hard_gate","plausibility","source_grades","precheck","allowance","session","post","emergency"],s=a3.a,r=0;r<9;++r){q=t[r]
if(!s.C(q))A.i(A.y("missing section: "+q))}t=a3.$ti.i("4?")
p=J.f(t.a(s.h(0,c)),"version")
if(J.v(p==null?"":p,""))A.i(A.y("meta.version required"))
if(!B.a.B(A.t(["draft","approved"],u.s),J.f(t.a(s.h(0,c)),"status")))A.i(A.y("meta.status must be draft|approved"))
if(J.v(J.f(t.a(s.h(0,c)),"status"),"approved")){p=u.g.a(J.f(t.a(s.h(0,c)),"approved_by"))
if(!J.ea(p==null?[]:p))A.i(A.y("approved bundle needs approved_by"))}o=t.a(s.h(0,"precheck"))
for(p=["systolic","diastolic","resting_hr"],n=J.A(o),m=u.j,r=0;r<3;++r){l=p[r]
A.ho(l,m.a(J.f(n.h(o,"bands"),l)))
k=J.f(t.a(s.h(0,"plausibility")),l)
j=J.A(k)
if(!(A.j(j.h(k,"min"))<A.j(j.h(k,"max"))))A.i(A.y("plausibility."+l+": min >= max"))}p=u.U
j=A.aC(p.a(n.h(o,"emergency_symptoms")),u.z)
B.a.O(j,p.a(n.h(o,"red_symptoms")))
B.a.O(j,p.a(n.h(o,"yellow_symptoms")))
if(j.length!==A.en(j,A.P(j).c).a)A.i(A.y("precheck symptom lists overlap"))
if(J.ec(m.a(n.h(o,"red_conditions"))).ak(J.ec(m.a(n.h(o,"yellow_conditions")))).a!==0)A.i(A.y("condition lists overlap"))
i=t.a(s.h(0,"session"))
p=J.A(i)
h=p.h(i,"ceiling_pct")
n=J.A(h)
m=!1
if(0<A.j(n.h(h,a))){j=n.h(h,a)
g=n.h(h,a0)
if(typeof j!=="number")return j.S()
if(typeof g!=="number")return A.bN(g)
if(j<=g){j=n.h(h,a0)
g=n.h(h,a1)
if(typeof j!=="number")return j.S()
if(typeof g!=="number")return A.bN(g)
if(j<=g){m=n.h(h,a1)
if(typeof m!=="number")return m.S()
m=m<=0.85}}}if(!m)A.i(A.y("ceiling_pct must satisfy initial <= escalated <= absolute_max <= 0.85"))
m=J.f(p.h(i,a2),"lower")
j=J.f(p.h(i,a2),"upper")
if(typeof m!=="number")return m.ao()
if(typeof j!=="number")return A.bN(j)
if(!(m<j))A.i(A.y("zone_pct lower >= upper"))
m=J.f(p.h(i,"rpe"),"step_down_at")
j=J.f(p.h(i,"rpe"),"stop_at")
if(typeof m!=="number")return m.ao()
if(typeof j!=="number")return A.bN(j)
if(!(m<j))A.i(A.y("rpe step_down_at must be < stop_at"))
m=p.h(i,"stop_ratio_over_ceiling")
if(typeof m!=="number")return m.aT()
if(!(m>1))A.i(A.y("stop_ratio_over_ceiling must be > 1"))
m=J.f(p.h(i,"sensor"),"fallback_checkin_interval_seconds")
j=p.h(i,"checkin_interval_seconds")
if(typeof m!=="number")return m.S()
if(typeof j!=="number")return A.bN(j)
if(!(m<=j))A.i(A.y("sensor fallback must ask at least as often as normal check-in"))
for(m=["A","B","C"],j=u.f,r=0;r<3;++r){f=m[r]
if(!j.a(p.h(i,"heart_rate_grades")).C(f))A.i(A.y("session.heart_rate_grades."+f+" missing"))}for(p=["GREEN","YELLOW","RED"],r=0;r<3;++r){e=p[r]
if(!j.a(t.a(s.h(0,b))).C(e))A.i(A.y("allowance."+e+" missing"))}if(!J.v(J.f(J.f(t.a(s.h(0,b)),"RED"),"allowed"),!1))A.i(A.y("RED must never allow exercise"))
d=J.f(J.f(t.a(s.h(0,b)),"YELLOW"),"hr_ceiling_pct_cap")
if(d!=null){t=n.h(h,a)
if(typeof d!=="number")return d.S()
if(typeof t!=="number")return A.bN(t)
if(!(d<=t))A.i(A.y("YELLOW hr cap must not exceed initial ceiling"))}},
cO:function cO(a){this.a=a},
dt:function dt(){},
du:function du(a){this.a=a},
cN:function cN(a,b,c){this.a=a
this.b=b
this.c=c},
I:function I(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
ch:function ch(a,b,c){var _=this
_.a=a
_.b=b
_.c=$
_.d=null
_.f=_.e=$
_.w=0
_.z=_.y=_.x=!1
_.as=_.Q=null
_.ay=_.ax=_.at=0
_.ch=!1
_.CW=c},
cX:function cX(){},
cR:function cR(a,b,c){this.a=a
this.b=b
this.c=c},
cT:function cT(a,b,c){this.a=a
this.b=b
this.c=c},
cU:function cU(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
cV:function cV(a,b){this.a=a
this.b=b},
cS:function cS(){},
cW:function cW(a,b){this.a=a
this.b=b},
cQ:function cQ(a){this.a=a},
eV(a){var t,s,r,q,p,o,n,m,l,k=null,j=A.F(a.h(0,"age")),i=u.g.a(a.h(0,"conditions"))
if(i==null)i=B.x
t=u.N
i=A.eo(J.bP(i,t),t)
s=J.v(a.h(0,"parq_risk"),!0)
r=J.v(a.h(0,"doctor_clearance"),!0)
q=A.b3(a.h(0,"device"))
p=J.v(a.h(0,"beta_blocker"),!0)
o=u.a5.a(a.h(0,"doctor_limits"))
t=o==null?k:o.a3(0,t,u.z)
o=t==null
n=A.aq(o?k:t.$ti.i("4?").a(t.a.h(0,"systolic_max")))
m=A.aq(o?k:t.$ti.i("4?").a(t.a.h(0,"diastolic_max")))
l=A.aq(o?k:t.$ti.i("4?").a(t.a.h(0,"resting_hr_max")))
return new A.cL(j,i,s,r,p,q,new A.cC(n,m,l,A.aq(o?k:t.$ti.i("4?").a(t.a.h(0,"exercise_hr_ceiling")))))},
hd(a){var t,s,r,q,p,o=A.t([],u.c)
for(t=a.length,s=u.N,r=u.z,q=0;q<a.length;a.length===t||(0,A.aM)(a),++q){p=a[q]
o.push(A.w(["t",p.a,"kind",p.b.b,"code",p.c,"detail",p.d],s,r))}return o},
eX(a){var t,s,r,q,p=A.t([],u.x)
for(t=a.length,s=u.q,r=0;r<a.length;a.length===t||(0,A.aM)(a),++r){q=a[r]
p.push(A.t([q.a.b,q.b],s))}return p},
hm(a,b){var t,s,r,q=null
try{s=B.b.D(A.w(["ok",!0,"result",B.b.aM(a.$1(u.P.a(B.b.aM(b,q))),q)],u.N,u.z),q)
return s}catch(r){t=A.e8(r)
s=B.b.D(A.w(["ok",!1,"error",A.l(t)],u.N,u.K),q)
return s}},
id(){var t={}
$.fh().N(0,new A.dD(t))
v.G.SafetyEngine=t},
dc:function dc(){},
dd:function dd(){},
de:function de(){},
df:function df(){},
dg:function dg(){},
dh:function dh(){},
di:function di(){},
dj:function dj(){},
dk:function dk(){},
dD:function dD(a){this.a=a},
dC:function dC(a){this.a=a},
f3(a){return v.mangledGlobalNames[a]},
ij(a){throw A.G(new A.aY("Field '"+a+"' has been assigned during initialization."),new Error())},
a1(){throw A.G(A.fF(""),new Error())},
ik(){throw A.G(A.fE(""),new Error())},
hn(a,b,c){u.Z.a(a)
if(A.F(c)>=1)return a.$1(b)
return a.$0()}},B={}
var w=[A,J,B]
var $={}
A.dM.prototype={}
J.c3.prototype={
R(a,b){return a===b},
gv(a){return A.br(a)},
k(a){return"Instance of '"+A.cf(a)+"'"},
gG(a){return A.aJ(A.dZ(this))}}
J.c5.prototype={
k(a){return String(a)},
gv(a){return a?519018:218159},
gG(a){return A.aJ(u.y)},
$iE:1,
$ia7:1}
J.be.prototype={
R(a,b){return null==b},
k(a){return"null"},
gv(a){return 0},
$iE:1}
J.bf.prototype={$iQ:1}
J.am.prototype={
gv(a){return 0},
k(a){return String(a)}}
J.ce.prototype={}
J.b0.prototype={}
J.a9.prototype={
k(a){var t=a[$.f5()]
if(t==null)t=a[$.e9()]
if(t==null)return this.aV(a)
return"JavaScript function for "+J.aj(t)},
$iaT:1}
J.aV.prototype={
gv(a){return 0},
k(a){return String(a)}}
J.aX.prototype={
gv(a){return 0},
k(a){return String(a)}}
J.o.prototype={
a2(a,b){return new A.a8(a,A.P(a).i("@<1>").q(b).i("a8<1,2>"))},
l(a,b){A.P(a).c.a(b)
a.$flags&1&&A.M(a,29)
a.push(b)},
O(a,b){var t
A.P(a).i("b<1>").a(b)
a.$flags&1&&A.M(a,"addAll",2)
if(Array.isArray(b)){this.aY(a,b)
return}for(t=J.cy(b);t.m();)a.push(t.gn())},
aY(a,b){var t,s
u.b.a(b)
t=b.length
if(t===0)return
if(a===b)throw A.a(A.N(a))
for(s=0;s<t;++s)a.push(b[s])},
U(a,b,c){var t=A.P(a)
return new A.R(a,t.q(c).i("1(2)").a(b),t.i("@<1>").q(c).i("R<1,2>"))},
L(a,b){return A.cY(a,b,null,A.P(a).c)},
ai(a,b){var t,s,r
A.P(a).i("a7(1)").a(b)
t=a.length
for(s=0;s<t;++s){r=a[s]
if(b.$1(r))return r
if(a.length!==t)throw A.a(A.N(a))}throw A.a(A.C())},
u(a,b){if(!(b>=0&&b<a.length))return A.d(a,b)
return a[b]},
gE(a){if(a.length>0)return a[0]
throw A.a(A.C())},
gF(a){var t=a.length
if(t>0)return a[t-1]
throw A.a(A.C())},
T(a,b,c,d,e){var t,s,r,q,p
A.P(a).i("b<1>").a(d)
a.$flags&2&&A.M(a,5)
A.cM(b,c,a.length)
t=c-b
if(t===0)return
A.V(e,"skipCount")
if(u.j.b(d)){s=d
r=e}else{s=J.dK(d,e).P(0,!1)
r=0}q=J.A(s)
if(r+t>q.gj(s))throw A.a(A.ek())
if(r<b)for(p=t-1;p>=0;--p)a[b+p]=q.h(s,r+p)
else for(p=0;p<t;++p)a[b+p]=q.h(s,r+p)},
aU(a,b){var t,s,r,q,p,o=A.P(a)
o.i("e(1,1)?").a(b)
a.$flags&2&&A.M(a,"sort")
t=a.length
if(t<2)return
if(b==null)b=J.hz()
if(t===2){s=a[0]
r=a[1]
o=b.$2(s,r)
if(typeof o!=="number")return o.aT()
if(o>0){a[0]=r
a[1]=s}return}q=0
if(o.c.b(null))for(p=0;p<a.length;++p)if(a[p]===void 0){a[p]=null;++q}a.sort(A.hX(b,2))
if(q>0)this.b9(a,q)},
a8(a){return this.aU(a,null)},
b9(a,b){var t,s=a.length
for(;t=s-1,s>0;s=t)if(a[t]===null){a[t]=void 0;--b
if(b===0)break}},
B(a,b){var t
for(t=0;t<a.length;++t)if(J.v(a[t],b))return!0
return!1},
gt(a){return a.length===0},
gJ(a){return a.length!==0},
k(a){return A.cF(a,"[","]")},
H(a){return A.en(a,A.P(a).c)},
gp(a){return new J.as(a,a.length,A.P(a).i("as<1>"))},
gv(a){return A.br(a)},
gj(a){return a.length},
h(a,b){A.F(b)
if(!(b>=0&&b<a.length))throw A.a(A.cw(a,b))
return a[b]},
A(a,b,c){A.P(a).c.a(c)
a.$flags&2&&A.M(a)
if(!(b>=0&&b<a.length))throw A.a(A.cw(a,b))
a[b]=c},
$ik:1,
$ib:1,
$in:1}
J.c4.prototype={
bB(a){var t,s,r
if(!Array.isArray(a))return null
t=a.$flags|0
if((t&4)!==0)s="const, "
else if((t&2)!==0)s="unmodifiable, "
else s=(t&1)!==0?"fixed, ":""
r="Instance of '"+A.cf(a)+"'"
if(s==="")return r
return r+" ("+s+"length: "+a.length+")"}}
J.cG.prototype={}
J.as.prototype={
gn(){var t=this.d
return t==null?this.$ti.c.a(t):t},
m(){var t,s=this,r=s.a,q=r.length
if(s.b!==q){r=A.aM(r)
throw A.a(r)}t=s.c
if(t>=q){s.d=null
return!1}s.d=r[t]
s.c=t+1
return!0},
$iH:1}
J.aU.prototype={
aL(a,b){var t
A.j(b)
if(a<b)return-1
else if(a>b)return 1
else if(a===b){if(a===0){t=this.gam(b)
if(this.gam(a)===t)return 0
if(this.gam(a))return-1
return 1}return 0}else if(isNaN(a)){if(isNaN(b))return 0
return 1}else return-1},
gam(a){return a===0?1/a<0:a<0},
aQ(a){var t
if(a>=-2147483648&&a<=2147483647)return a|0
if(isFinite(a)){t=a<0?Math.ceil(a):Math.floor(a)
return t+0}throw A.a(A.b1(""+a+".toInt()"))},
bl(a){var t,s
if(a>=0){if(a<=2147483647){t=a|0
return a===t?t:t+1}}else if(a>=-2147483648)return a|0
s=Math.ceil(a)
if(isFinite(s))return s
throw A.a(A.b1(""+a+".ceil()"))},
aN(a){var t,s
if(a>=0){if(a<=2147483647)return a|0}else if(a>=-2147483648){t=a|0
return a===t?t:t-1}s=Math.floor(a)
if(isFinite(s))return s
throw A.a(A.b1(""+a+".floor()"))},
a5(a){if(a>0){if(a!==1/0)return Math.round(a)}else if(a>-1/0)return 0-Math.round(0-a)
throw A.a(A.b1(""+a+".round()"))},
k(a){if(a===0&&1/a<0)return"-0.0"
else return""+a},
gv(a){var t,s,r,q,p=a|0
if(a===p)return p&536870911
t=Math.abs(a)
s=Math.log(t)/0.6931471805599453|0
r=Math.pow(2,s)
q=t<1?t/r:r/t
return((q*9007199254740992|0)+(q*3542243181176521|0))*599197+s*1259&536870911},
bf(a,b){return(a|0)===a?a/b|0:this.bg(a,b)},
bg(a,b){var t=a/b
if(t>=-2147483648&&t<=2147483647)return t|0
if(t>0){if(t!==1/0)return Math.floor(t)}else if(t>-1/0)return Math.ceil(t)
throw A.a(A.b1("Result of truncating division is "+A.l(t)+": "+A.l(a)+" ~/ "+b))},
aH(a,b){var t
if(a>0)t=this.bc(a,b)
else{t=b>31?31:b
t=a>>t>>>0}return t},
bc(a,b){return b>31?0:a>>>b},
gG(a){return A.aJ(u.H)},
$ial:1,
$iq:1}
J.bd.prototype={
gG(a){return A.aJ(u.S)},
$iE:1,
$ie:1}
J.c6.prototype={
gG(a){return A.aJ(u.i)},
$iE:1}
J.az.prototype={
X(a,b,c){return a.substring(b,A.cM(b,c,a.length))},
aL(a,b){var t
A.L(b)
if(a===b)t=0
else t=a<b?-1:1
return t},
k(a){return a},
gv(a){var t,s,r
for(t=a.length,s=0,r=0;r<t;++r){s=s+a.charCodeAt(r)&536870911
s=s+((s&524287)<<10)&536870911
s^=s>>6}s=s+((s&67108863)<<3)&536870911
s^=s>>11
return s+((s&16383)<<15)&536870911},
gG(a){return A.aJ(u.N)},
gj(a){return a.length},
h(a,b){A.F(b)
if(!(b.bG(0,0)&&b.ao(0,a.length)))throw A.a(A.cw(a,b))
return a[b]},
$iE:1,
$ial:1,
$ic:1}
A.an.prototype={
gp(a){return new A.b8(J.cy(this.gI()),A.h(this).i("b8<1,2>"))},
gj(a){return J.aN(this.gI())},
gt(a){return J.fp(this.gI())},
gJ(a){return J.ea(this.gI())},
L(a,b){var t=A.h(this)
return A.dL(J.dK(this.gI(),b),t.c,t.y[1])},
u(a,b){return A.h(this).y[1].a(J.dJ(this.gI(),b))},
gE(a){return A.h(this).y[1].a(J.fo(this.gI()))},
gF(a){return A.h(this).y[1].a(J.fq(this.gI()))},
B(a,b){return J.bQ(this.gI(),b)},
k(a){return J.aj(this.gI())}}
A.b8.prototype={
m(){return this.a.m()},
gn(){return this.$ti.y[1].a(this.a.gn())},
$iH:1}
A.at.prototype={
gI(){return this.a}}
A.bB.prototype={$ik:1}
A.bA.prototype={
h(a,b){return this.$ti.y[1].a(J.f(this.a,A.F(b)))},
A(a,b,c){var t=this.$ti
J.fj(this.a,b,t.c.a(t.y[1].a(c)))},
$ik:1,
$in:1}
A.a8.prototype={
a2(a,b){return new A.a8(this.a,this.$ti.i("@<1>").q(b).i("a8<1,2>"))},
gI(){return this.a}}
A.au.prototype={
a3(a,b,c){return new A.au(this.a,this.$ti.i("@<1,2>").q(b).q(c).i("au<1,2,3,4>"))},
C(a){return this.a.C(a)},
h(a,b){return this.$ti.i("4?").a(this.a.h(0,b))},
N(a,b){this.a.N(0,new A.cA(this,this.$ti.i("~(3,4)").a(b)))},
gK(){var t=this.$ti
return A.dL(this.a.gK(),t.c,t.y[2])},
gj(a){var t=this.a
return t.gj(t)},
gt(a){var t=this.a
return t.gt(t)}}
A.cA.prototype={
$2(a,b){var t=this.a.$ti
t.c.a(a)
t.y[1].a(b)
this.b.$2(t.y[2].a(a),t.y[3].a(b))},
$S(){return this.a.$ti.i("~(1,2)")}}
A.aY.prototype={
k(a){return"LateInitializationError: "+this.a}}
A.cP.prototype={}
A.k.prototype={}
A.D.prototype={
gp(a){var t=this
return new A.aB(t,t.gj(t),A.h(t).i("aB<D.E>"))},
gt(a){return this.gj(this)===0},
gE(a){if(this.gj(this)===0)throw A.a(A.C())
return this.u(0,0)},
gF(a){var t=this
if(t.gj(t)===0)throw A.a(A.C())
return t.u(0,t.gj(t)-1)},
B(a,b){var t,s=this,r=s.gj(s)
for(t=0;t<r;++t){if(J.v(s.u(0,t),b))return!0
if(r!==s.gj(s))throw A.a(A.N(s))}return!1},
aP(a,b){var t,s,r,q=this,p=q.gj(q)
if(b.length!==0){if(p===0)return""
t=A.l(q.u(0,0))
if(p!==q.gj(q))throw A.a(A.N(q))
for(s=t,r=1;r<p;++r){s=s+b+A.l(q.u(0,r))
if(p!==q.gj(q))throw A.a(A.N(q))}return s.charCodeAt(0)==0?s:s}else{for(r=0,s="";r<p;++r){s+=A.l(q.u(0,r))
if(p!==q.gj(q))throw A.a(A.N(q))}return s.charCodeAt(0)==0?s:s}},
U(a,b,c){var t=A.h(this)
return new A.R(this,t.q(c).i("1(D.E)").a(b),t.i("@<D.E>").q(c).i("R<1,2>"))},
aO(a,b,c,d){var t,s,r,q=this
d.a(b)
A.h(q).q(d).i("1(1,D.E)").a(c)
t=q.gj(q)
for(s=b,r=0;r<t;++r){s=c.$2(s,q.u(0,r))
if(t!==q.gj(q))throw A.a(A.N(q))}return s},
L(a,b){return A.cY(this,b,null,A.h(this).i("D.E"))},
P(a,b){var t=A.aC(this,A.h(this).i("D.E"))
return t},
a6(a){return this.P(0,!0)},
H(a){var t,s=this,r=A.cc(A.h(s).i("D.E"))
for(t=0;t<s.gj(s);++t)r.l(0,s.u(0,t))
return r}}
A.bx.prototype={
gb1(){var t=J.aN(this.a),s=this.c
if(s==null||s>t)return t
return s},
gbd(){var t=J.aN(this.a),s=this.b
if(s>t)return t
return s},
gj(a){var t,s=J.aN(this.a),r=this.b
if(r>=s)return 0
t=this.c
if(t==null||t>=s)return s-r
return t-r},
u(a,b){var t=this,s=t.gbd()+b
if(b<0||s>=t.gb1())throw A.a(A.c2(b,t.gj(0),t,null,"index"))
return J.dJ(t.a,s)},
L(a,b){var t,s,r=this
A.V(b,"count")
t=r.b+b
s=r.c
if(s!=null&&t>=s)return new A.ax(r.$ti.i("ax<1>"))
return A.cY(r.a,t,s,r.$ti.c)},
P(a,b){var t,s,r,q=this,p=q.b,o=q.a,n=J.A(o),m=n.gj(o),l=q.c
if(l!=null&&l<m)m=l
t=m-p
if(t<=0){o=J.el(0,q.$ti.c)
return o}s=A.cI(t,n.u(o,p),!1,q.$ti.c)
for(r=1;r<t;++r){B.a.A(s,r,n.u(o,p+r))
if(n.gj(o)<m)throw A.a(A.N(q))}return s}}
A.aB.prototype={
gn(){var t=this.d
return t==null?this.$ti.c.a(t):t},
m(){var t,s=this,r=s.a,q=J.A(r),p=q.gj(r)
if(s.b!==p)throw A.a(A.N(r))
t=s.c
if(t>=p){s.d=null
return!1}s.d=q.u(r,t);++s.c
return!0},
$iH:1}
A.aD.prototype={
gp(a){var t=this.a
return new A.bk(t.gp(t),this.b,A.h(this).i("bk<1,2>"))},
gj(a){var t=this.a
return t.gj(t)},
gt(a){var t=this.a
return t.gt(t)},
gE(a){var t=this.a
return this.b.$1(t.gE(t))},
gF(a){var t=this.a
return this.b.$1(t.gF(t))},
u(a,b){var t=this.a
return this.b.$1(t.u(t,b))}}
A.aw.prototype={$ik:1}
A.bk.prototype={
m(){var t=this,s=t.b
if(s.m()){t.a=t.c.$1(s.gn())
return!0}t.a=null
return!1},
gn(){var t=this.a
return t==null?this.$ti.y[1].a(t):t},
$iH:1}
A.R.prototype={
gj(a){return J.aN(this.a)},
u(a,b){return this.b.$1(J.dJ(this.a,b))}}
A.ae.prototype={
L(a,b){A.cz(b,"count",u.S)
A.V(b,"count")
return new A.ae(this.a,this.b+b,A.h(this).i("ae<1>"))},
gp(a){var t=this.a
return new A.bv(t.gp(t),this.b,A.h(this).i("bv<1>"))}}
A.aS.prototype={
gj(a){var t=this.a,s=t.gj(t)-this.b
if(s>=0)return s
return 0},
L(a,b){A.cz(b,"count",u.S)
A.V(b,"count")
return new A.aS(this.a,this.b+b,this.$ti)},
$ik:1}
A.bv.prototype={
m(){var t,s
for(t=this.a,s=0;s<this.b;++s)t.m()
this.b=0
return t.m()},
gn(){return this.a.gn()},
$iH:1}
A.ax.prototype={
gp(a){return B.P},
gt(a){return!0},
gj(a){return 0},
gE(a){throw A.a(A.C())},
gF(a){throw A.a(A.C())},
u(a,b){throw A.a(A.a6(b,0,0,"index",null))},
B(a,b){return!1},
U(a,b,c){this.$ti.q(c).i("1(2)").a(b)
return new A.ax(c.i("ax<0>"))},
L(a,b){A.V(b,"count")
return this},
H(a){return A.cc(this.$ti.c)}}
A.bb.prototype={
m(){return!1},
gn(){throw A.a(A.C())},
$iH:1}
A.ay.prototype={}
A.bM.prototype={}
A.r.prototype={$r:"+(1,2)",$s:1}
A.b9.prototype={
a3(a,b,c){var t=A.h(this)
return A.ep(this,t.c,t.y[1],b,c)},
gt(a){return this.gj(this)===0},
k(a){return A.dQ(this)},
$iJ:1}
A.av.prototype={
gj(a){return this.b.length},
gaE(){var t=this.$keys
if(t==null){t=Object.keys(this.a)
this.$keys=t}return t},
C(a){if(typeof a!="string")return!1
if("__proto__"===a)return!1
return this.a.hasOwnProperty(a)},
h(a,b){if(!this.C(b))return null
return this.b[this.a[b]]},
N(a,b){var t,s,r,q
this.$ti.i("~(1,2)").a(b)
t=this.gaE()
s=this.b
for(r=t.length,q=0;q<r;++q)b.$2(t[q],s[q])},
gK(){return new A.bC(this.gaE(),this.$ti.i("bC<1>"))}}
A.bC.prototype={
gj(a){return this.a.length},
gt(a){return 0===this.a.length},
gJ(a){return 0!==this.a.length},
gp(a){var t=this.a
return new A.ai(t,t.length,this.$ti.i("ai<1>"))}}
A.ai.prototype={
gn(){var t=this.d
return t==null?this.$ti.c.a(t):t},
m(){var t=this,s=t.c
if(s>=t.b){t.d=null
return!1}t.d=t.a[s]
t.c=s+1
return!0},
$iH:1}
A.aP.prototype={
l(a,b){A.h(this).c.a(b)
A.fA()}}
A.ba.prototype={
gj(a){return this.b},
gt(a){return this.b===0},
gJ(a){return this.b!==0},
gp(a){var t,s=this,r=s.$keys
if(r==null){r=Object.keys(s.a)
s.$keys=r}t=r
return new A.ai(t,t.length,s.$ti.i("ai<1>"))},
B(a,b){if(typeof b!="string")return!1
if("__proto__"===b)return!1
return this.a.hasOwnProperty(b)}}
A.bc.prototype={
gj(a){return this.a.length},
gt(a){return this.a.length===0},
gJ(a){return this.a.length!==0},
gp(a){var t=this.a
return new A.ai(t,t.length,this.$ti.i("ai<1>"))},
b4(){var t,s,r,q,p=this,o=p.$map
if(o==null){o=new A.bg(p.$ti.i("bg<1,1>"))
for(t=p.a,s=t.length,r=0;r<t.length;t.length===s||(0,A.aM)(t),++r){q=t[r]
o.A(0,q,q)}p.$map=o}return o},
B(a,b){return this.b4().C(b)}}
A.bt.prototype={}
A.d_.prototype={
M(a){var t,s,r=this,q=new RegExp(r.a).exec(a)
if(q==null)return null
t=Object.create(null)
s=r.b
if(s!==-1)t.arguments=q[s+1]
s=r.c
if(s!==-1)t.argumentsExpr=q[s+1]
s=r.d
if(s!==-1)t.expr=q[s+1]
s=r.e
if(s!==-1)t.method=q[s+1]
s=r.f
if(s!==-1)t.receiver=q[s+1]
return t}}
A.bq.prototype={
k(a){return"Null check operator used on a null value"}}
A.c7.prototype={
k(a){var t,s=this,r="NoSuchMethodError: method not found: '",q=s.b
if(q==null)return"NoSuchMethodError: "+s.a
t=s.c
if(t==null)return r+q+"' ("+s.a+")"
return r+q+"' on '"+t+"' ("+s.a+")"}}
A.cl.prototype={
k(a){var t=this.a
return t.length===0?"Error":"Error: "+t}}
A.cK.prototype={
k(a){return"Throw of null ('"+(this.a===null?"null":"undefined")+"' from JavaScript)"}}
A.ak.prototype={
k(a){var t=this.constructor,s=t==null?null:t.name
return"Closure '"+A.f4(s==null?"unknown":s)+"'"},
$iaT:1,
gbF(){return this},
$C:"$1",
$R:1,
$D:null}
A.bT.prototype={$C:"$2",$R:2}
A.cj.prototype={}
A.ci.prototype={
k(a){var t=this.$static_name
if(t==null)return"Closure of unknown static method"
return"Closure '"+A.f4(t)+"'"}}
A.aO.prototype={
R(a,b){if(b==null)return!1
if(this===b)return!0
if(!(b instanceof A.aO))return!1
return this.$_target===b.$_target&&this.a===b.a},
gv(a){return(A.e7(this.a)^A.br(this.$_target))>>>0},
k(a){return"Closure '"+this.$_name+"' of "+("Instance of '"+A.cf(this.a)+"'")}}
A.cg.prototype={
k(a){return"RuntimeError: "+this.a}}
A.aa.prototype={
gj(a){return this.a},
gt(a){return this.a===0},
gK(){return new A.aA(this,A.h(this).i("aA<1>"))},
C(a){var t,s
if(typeof a=="string"){t=this.b
if(t==null)return!1
return t[a]!=null}else if(typeof a=="number"&&(a&0x3fffffff)===a){s=this.c
if(s==null)return!1
return s[a]!=null}else return this.bs(a)},
bs(a){var t=this.d
if(t==null)return!1
return this.a4(this.aB(t,a),a)>=0},
h(a,b){var t,s,r,q,p=null
if(typeof b=="string"){t=this.b
if(t==null)return p
s=t[b]
r=s==null?p:s.b
return r}else if(typeof b=="number"&&(b&0x3fffffff)===b){q=this.c
if(q==null)return p
s=q[b]
r=s==null?p:s.b
return r}else return this.bt(b)},
bt(a){var t,s,r=this.d
if(r==null)return null
t=this.aB(r,a)
s=this.a4(t,a)
if(s<0)return null
return t[s].b},
A(a,b,c){var t,s,r,q,p,o,n=this,m=A.h(n)
m.c.a(b)
m.y[1].a(c)
if(typeof b=="string"){t=n.b
n.aq(t==null?n.b=n.ad():t,b,c)}else if(typeof b=="number"&&(b&0x3fffffff)===b){s=n.c
n.aq(s==null?n.c=n.ad():s,b,c)}else{r=n.d
if(r==null)r=n.d=n.ad()
q=n.aj(b)
p=r[q]
if(p==null)r[q]=[n.ae(b,c)]
else{o=n.a4(p,b)
if(o>=0)p[o].b=c
else p.push(n.ae(b,c))}}},
N(a,b){var t,s,r=this
A.h(r).i("~(1,2)").a(b)
t=r.e
s=r.r
while(t!=null){b.$2(t.a,t.b)
if(s!==r.r)throw A.a(A.N(r))
t=t.c}},
aq(a,b,c){var t,s=A.h(this)
s.c.a(b)
s.y[1].a(c)
t=a[b]
if(t==null)a[b]=this.ae(b,c)
else t.b=c},
ae(a,b){var t=this,s=A.h(t),r=new A.cH(s.c.a(a),s.y[1].a(b))
if(t.e==null)t.e=t.f=r
else t.f=t.f.c=r;++t.a
t.r=t.r+1&1073741823
return r},
aj(a){return J.a2(a)&1073741823},
aB(a,b){return a[this.aj(b)]},
a4(a,b){var t,s
if(a==null)return-1
t=a.length
for(s=0;s<t;++s)if(J.v(a[s].a,b))return s
return-1},
k(a){return A.dQ(this)},
ad(){var t=Object.create(null)
t["<non-identifier-key>"]=t
delete t["<non-identifier-key>"]
return t},
$idO:1}
A.cH.prototype={}
A.aA.prototype={
gj(a){return this.a.a},
gt(a){return this.a.a===0},
gp(a){var t=this.a
return new A.bi(t,t.r,t.e,this.$ti.i("bi<1>"))},
B(a,b){return this.a.C(b)}}
A.bi.prototype={
gn(){return this.d},
m(){var t,s=this,r=s.a
if(s.b!==r.r)throw A.a(A.N(r))
t=s.c
if(t==null){s.d=null
return!1}else{s.d=t.a
s.c=t.c
return!0}},
$iH:1}
A.bg.prototype={
aj(a){return A.hW(a)&1073741823},
a4(a,b){var t,s
if(a==null)return-1
t=a.length
for(s=0;s<t;++s)if(J.v(a[s].a,b))return s
return-1}}
A.dy.prototype={
$1(a){return this.a(a)},
$S:2}
A.dz.prototype={
$2(a,b){return this.a(a,b)},
$S:6}
A.dA.prototype={
$1(a){return this.a(A.L(a))},
$S:7}
A.ao.prototype={
k(a){return this.aI(!1)},
aI(a){var t,s,r,q,p,o=this.b2(),n=this.aC(),m=(a?"Record ":"")+"("
for(t=o.length,s="",r=0;r<t;++r,s=", "){m+=s
q=o[r]
if(typeof q=="string")m=m+q+": "
if(!(r<n.length))return A.d(n,r)
p=n[r]
m=a?m+A.er(p):m+A.l(p)}m+=")"
return m.charCodeAt(0)==0?m:m},
b2(){var t,s=this.$s
while($.d7.length<=s)B.a.l($.d7,null)
t=$.d7[s]
if(t==null){t=this.b_()
B.a.A($.d7,s,t)}return t},
b_(){var t,s,r,q=this.$r,p=q.indexOf("("),o=q.substring(1,p),n=q.substring(p),m=n==="()"?0:n.replace(/[^,]/g,"").length+1,l=A.t(new Array(m),u.G)
for(t=0;t<m;++t)l[t]=t
if(o!==""){s=o.split(",")
t=s.length
for(r=m;t>0;){--r;--t
B.a.A(l,r,s[t])}}l=A.fH(l,!1,u.K)
l.$flags=3
return l}}
A.b2.prototype={
aC(){return[this.a,this.b]},
R(a,b){if(b==null)return!1
return b instanceof A.b2&&this.$s===b.$s&&J.v(this.a,b.a)&&J.v(this.b,b.b)},
gv(a){return A.fL(this.$s,this.a,this.b,B.r)}}
A.aE.prototype={
gG(a){return B.aH},
bj(a,b,c){var t
A.dp(a,b,c)
t=new Uint8Array(a,b)
return t},
aK(a){return this.bj(a,0,null)},
a1(a,b,c){var t
A.dp(a,b,c)
t=new DataView(a,b)
return t},
aJ(a){return this.a1(a,0,null)},
$iE:1,
$iaE:1}
A.bl.prototype={
gW(a){if(((a.$flags|0)&2)!==0)return new A.d9(a.buffer)
else return a.buffer},
b6(a,b,c,d){var t=A.a6(b,0,c,d,null)
throw A.a(t)},
au(a,b,c,d){if(b>>>0!==b||b>c)this.b6(a,b,c,d)}}
A.d9.prototype={
aK(a){var t=A.fK(this.a,0,null)
t.$flags=3
return t},
a1(a,b,c){var t=A.fJ(this.a,b,c)
t.$flags=3
return t},
aJ(a){return this.a1(0,0,null)}}
A.cd.prototype={
gG(a){return B.aI},
$iE:1,
$ieh:1}
A.a5.prototype={
gj(a){return a.length},
$iaW:1}
A.ab.prototype={
A(a,b,c){A.F(c)
a.$flags&2&&A.M(a)
A.dn(b,a,a.length)
a[b]=c},
T(a,b,c,d,e){var t,s,r,q
u.Y.a(d)
a.$flags&2&&A.M(a,5)
if(u.E.b(d)){t=a.length
this.au(a,b,t,"start")
this.au(a,c,t,"end")
if(b>c)A.i(A.a6(b,0,c,null,null))
s=c-b
if(e<0)A.i(A.X(e))
r=d.length
if(r-e<s)A.i(A.af("Not enough elements"))
q=e!==0||r!==s?d.subarray(e,e+s):d
a.set(q,b)
return}this.aW(a,b,c,d,e)},
$ik:1,
$ib:1,
$in:1}
A.bm.prototype={
gG(a){return B.aK},
h(a,b){A.F(b)
A.dn(b,a,a.length)
return a[b]},
$iE:1}
A.bn.prototype={
gG(a){return B.aL},
h(a,b){A.F(b)
A.dn(b,a,a.length)
return a[b]},
$iE:1,
$idS:1}
A.bo.prototype={
gG(a){return B.aM},
gj(a){return a.length},
h(a,b){A.F(b)
A.dn(b,a,a.length)
return a[b]},
$iE:1,
$idT:1}
A.bE.prototype={}
A.bF.prototype={}
A.Z.prototype={
i(a){return A.bL(v.typeUniverse,this,a)},
q(a){return A.eH(v.typeUniverse,this,a)}}
A.cp.prototype={}
A.cv.prototype={
k(a){return A.S(this.a,null)}}
A.co.prototype={
k(a){return this.a}}
A.bH.prototype={}
A.aF.prototype={
af(){return new A.aF(A.h(this).i("aF<1>"))},
gp(a){var t=this,s=new A.aG(t,t.r,A.h(t).i("aG<1>"))
s.c=t.e
return s},
gj(a){return this.a},
gt(a){return this.a===0},
gJ(a){return this.a!==0},
B(a,b){var t,s
if(typeof b=="string"&&b!=="__proto__"){t=this.b
if(t==null)return!1
return u.L.a(t[b])!=null}else if(typeof b=="number"&&(b&1073741823)===b){s=this.c
if(s==null)return!1
return u.L.a(s[b])!=null}else return this.b0(b)},
b0(a){var t=this.d
if(t==null)return!1
return this.aA(t[this.aw(a)],a)>=0},
gE(a){var t=this.e
if(t==null)throw A.a(A.af("No elements"))
return A.h(this).c.a(t.a)},
gF(a){var t=this.f
if(t==null)throw A.a(A.af("No elements"))
return A.h(this).c.a(t.a)},
l(a,b){var t,s,r=this
A.h(r).c.a(b)
if(typeof b=="string"&&b!=="__proto__"){t=r.b
return r.av(t==null?r.b=A.dU():t,b)}else if(typeof b=="number"&&(b&1073741823)===b){s=r.c
return r.av(s==null?r.c=A.dU():s,b)}else return r.aX(b)},
aX(a){var t,s,r,q=this
A.h(q).c.a(a)
t=q.d
if(t==null)t=q.d=A.dU()
s=q.aw(a)
r=t[s]
if(r==null)t[s]=[q.aa(a)]
else{if(q.aA(r,a)>=0)return!1
r.push(q.aa(a))}return!0},
av(a,b){A.h(this).c.a(b)
if(u.L.a(a[b])!=null)return!1
a[b]=this.aa(b)
return!0},
b7(){this.r=this.r+1&1073741823},
aa(a){var t,s=this,r=new A.cs(A.h(s).c.a(a))
if(s.e==null)s.e=s.f=r
else{t=s.f
t.toString
r.c=t
s.f=t.b=r}++s.a
s.b7()
return r},
aw(a){return J.a2(a)&1073741823},
aA(a,b){var t,s
if(a==null)return-1
t=a.length
for(s=0;s<t;++s)if(J.v(a[s].a,b))return s
return-1}}
A.cs.prototype={}
A.aG.prototype={
gn(){var t=this.d
return t==null?this.$ti.c.a(t):t},
m(){var t=this,s=t.c,r=t.a
if(t.b!==r.r)throw A.a(A.N(r))
else if(s==null){t.d=null
return!1}else{t.d=t.$ti.i("1?").a(s.a)
t.c=s.b
return!0}},
$iH:1}
A.x.prototype={
gp(a){return new A.aB(a,this.gj(a),A.a0(a).i("aB<x.E>"))},
u(a,b){return this.h(a,b)},
gt(a){return this.gj(a)===0},
gJ(a){return!this.gt(a)},
gE(a){if(this.gj(a)===0)throw A.a(A.C())
return this.h(a,0)},
gF(a){if(this.gj(a)===0)throw A.a(A.C())
return this.h(a,this.gj(a)-1)},
B(a,b){var t,s=this.gj(a)
for(t=0;t<s;++t){if(J.v(this.h(a,t),b))return!0
if(s!==this.gj(a))throw A.a(A.N(a))}return!1},
ai(a,b){var t,s,r
A.a0(a).i("a7(x.E)").a(b)
t=this.gj(a)
for(s=0;s<t;++s){r=this.h(a,s)
if(b.$1(r))return r
if(t!==this.gj(a))throw A.a(A.N(a))}throw A.a(A.C())},
U(a,b,c){var t=A.a0(a)
return new A.R(a,t.q(c).i("1(x.E)").a(b),t.i("@<x.E>").q(c).i("R<1,2>"))},
L(a,b){return A.cY(a,b,null,A.a0(a).i("x.E"))},
H(a){var t,s=A.cc(A.a0(a).i("x.E"))
for(t=0;t<this.gj(a);++t)s.l(0,this.h(a,t))
return s},
a2(a,b){return new A.a8(a,A.a0(a).i("@<x.E>").q(b).i("a8<1,2>"))},
T(a,b,c,d,e){var t,s,r,q,p
A.a0(a).i("b<x.E>").a(d)
A.cM(b,c,this.gj(a))
t=c-b
if(t===0)return
A.V(e,"skipCount")
if(u.j.b(d)){s=e
r=d}else{r=J.dK(d,e).P(0,!1)
s=0}if(s+t>r.length)throw A.a(A.ek())
if(s<b)for(q=t-1;q>=0;--q){p=s+q
if(!(p>=0&&p<r.length))return A.d(r,p)
this.A(a,b+q,r[p])}else for(q=0;q<t;++q){p=s+q
if(!(p>=0&&p<r.length))return A.d(r,p)
this.A(a,b+q,r[p])}},
k(a){return A.cF(a,"[","]")}}
A.z.prototype={
a3(a,b,c){var t=A.h(this)
return A.ep(this,t.i("z.K"),t.i("z.V"),b,c)},
N(a,b){var t,s,r,q=A.h(this)
q.i("~(z.K,z.V)").a(b)
for(t=this.gK(),t=t.gp(t),q=q.i("z.V");t.m();){s=t.gn()
r=this.h(0,s)
b.$2(s,r==null?q.a(r):r)}},
C(a){return this.gK().B(0,a)},
gj(a){var t=this.gK()
return t.gj(t)},
gt(a){var t=this.gK()
return t.gt(t)},
k(a){return A.dQ(this)},
$iJ:1}
A.cJ.prototype={
$2(a,b){var t,s=this.a
if(!s.a)this.b.a+=", "
s.a=!1
s=this.b
t=A.l(a)
s.a=(s.a+=t)+": "
t=A.l(b)
s.a+=t},
$S:3}
A.bj.prototype={
gp(a){var t=this
return new A.bD(t,t.c,t.d,t.b,t.$ti.i("bD<1>"))},
gt(a){return this.b===this.c},
gj(a){return(this.c-this.b&this.a.length-1)>>>0},
gE(a){var t,s=this,r=s.b
if(r===s.c)throw A.a(A.C())
t=s.a
if(!(r<t.length))return A.d(t,r)
r=t[r]
return r==null?s.$ti.c.a(r):r},
gF(a){var t,s=this,r=s.b,q=s.c
if(r===q)throw A.a(A.C())
r=s.a
t=r.length
q=(q-1&t-1)>>>0
if(!(q>=0&&q<t))return A.d(r,q)
q=r[q]
return q==null?s.$ti.c.a(q):q},
u(a,b){var t,s,r=this,q=r.gj(0)
if(0>b||b>=q)A.i(A.c2(b,q,r,null,"index"))
q=r.a
t=q.length
s=(r.b+b&t-1)>>>0
if(!(s>=0&&s<t))return A.d(q,s)
s=q[s]
return s==null?r.$ti.c.a(s):s},
k(a){return A.cF(this,"{","}")},
$ifO:1}
A.bD.prototype={
gn(){var t=this.e
return t==null?this.$ti.c.a(t):t},
m(){var t,s,r=this,q=r.a
if(r.c!==q.d)A.i(A.N(q))
t=r.d
if(t===r.b){r.e=null
return!1}q=q.a
s=q.length
if(!(t<s))return A.d(q,t)
r.e=q[t]
r.d=(t+1&s-1)>>>0
return!0},
$iH:1}
A.ad.prototype={
gt(a){return this.gj(this)===0},
gJ(a){return this.gj(this)!==0},
O(a,b){var t
A.h(this).i("b<1>").a(b)
for(t=b.gp(b);t.m();)this.l(0,t.gn())},
P(a,b){var t=A.aC(this,A.h(this).c)
return t},
a6(a){return this.P(0,!0)},
U(a,b,c){var t=A.h(this)
return new A.aw(this,t.q(c).i("1(2)").a(b),t.i("@<1>").q(c).i("aw<1,2>"))},
k(a){return A.cF(this,"{","}")},
L(a,b){return A.et(this,b,A.h(this).c)},
gE(a){var t=this.gp(this)
if(!t.m())throw A.a(A.C())
return t.gn()},
gF(a){var t,s=this.gp(this)
if(!s.m())throw A.a(A.C())
do t=s.gn()
while(s.m())
return t},
u(a,b){var t,s
A.V(b,"index")
t=this.gp(this)
for(s=b;t.m();){if(s===0)return t.gn();--s}throw A.a(A.c2(b,b-s,this,null,"index"))},
$ik:1,
$ib:1,
$iac:1}
A.bG.prototype={
bq(a){var t,s,r,q=this,p=q.af()
for(t=A.ey(q,q.r,A.h(q).c),s=t.$ti.c;t.m();){r=t.d
if(r==null)r=s.a(r)
if(!a.B(0,r))p.l(0,r)}return p},
ak(a){var t,s,r,q=this,p=q.af()
for(t=A.ey(q,q.r,A.h(q).c),s=t.$ti.c;t.m();){r=t.d
if(r==null)r=s.a(r)
if(a.B(0,r))p.l(0,r)}return p},
H(a){var t=this.af()
t.O(0,this)
return t}}
A.cq.prototype={
h(a,b){var t,s=this.b
if(s==null)return this.c.h(0,b)
else if(typeof b!="string")return null
else{t=s[b]
return typeof t=="undefined"?this.b8(b):t}},
gj(a){return this.b==null?this.c.a:this.Z().length},
gt(a){return this.gj(0)===0},
gK(){if(this.b==null){var t=this.c
return new A.aA(t,A.h(t).i("aA<1>"))}return new A.cr(this)},
C(a){if(this.b==null)return this.c.C(a)
return Object.prototype.hasOwnProperty.call(this.a,a)},
N(a,b){var t,s,r,q,p=this
u.cQ.a(b)
if(p.b==null)return p.c.N(0,b)
t=p.Z()
for(s=0;s<t.length;++s){r=t[s]
q=p.b[r]
if(typeof q=="undefined"){q=A.dq(p.a[r])
p.b[r]=q}b.$2(r,q)
if(t!==p.c)throw A.a(A.N(p))}},
Z(){var t=u.g.a(this.c)
if(t==null)t=this.c=A.t(Object.keys(this.a),u.s)
return t},
b8(a){var t
if(!Object.prototype.hasOwnProperty.call(this.a,a))return null
t=A.dq(this.a[a])
return this.b[a]=t}}
A.cr.prototype={
gj(a){return this.a.gj(0)},
u(a,b){var t=this.a
if(t.b==null)t=t.gK().u(0,b)
else{t=t.Z()
if(!(b>=0&&b<t.length))return A.d(t,b)
t=t[b]}return t},
gp(a){var t=this.a
if(t.b==null){t=t.gK()
t=t.gp(t)}else{t=t.Z()
t=new J.as(t,t.length,A.P(t).i("as<1>"))}return t},
B(a,b){return this.a.C(b)}}
A.bU.prototype={}
A.aQ.prototype={}
A.bh.prototype={
k(a){var t=A.c_(this.a)
return(this.b!=null?"Converting object to an encodable object failed:":"Converting object did not return an encodable object:")+" "+t}}
A.c9.prototype={
k(a){return"Cyclic error in JSON stringify"}}
A.c8.prototype={
aM(a,b){var t=A.hM(a,this.gbp().a)
return t},
D(a,b){var t=A.fW(a,this.gbr().b,null)
return t},
gbr(){return B.a5},
gbp(){return B.a4}}
A.cb.prototype={}
A.ca.prototype={}
A.d5.prototype={
aS(a){var t,s,r,q,p,o,n=a.length
for(t=this.c,s=0,r=0;r<n;++r){q=a.charCodeAt(r)
if(q>92){if(q>=55296){p=q&64512
if(p===55296){o=r+1
o=!(o<n&&(a.charCodeAt(o)&64512)===56320)}else o=!1
if(!o)if(p===56320){p=r-1
p=!(p>=0&&(a.charCodeAt(p)&64512)===55296)}else p=!1
else p=!0
if(p){if(r>s)t.a+=B.m.X(a,s,r)
s=r+1
p=A.K(92)
t.a+=p
p=A.K(117)
t.a+=p
p=A.K(100)
t.a+=p
p=q>>>8&15
p=A.K(p<10?48+p:87+p)
t.a+=p
p=q>>>4&15
p=A.K(p<10?48+p:87+p)
t.a+=p
p=q&15
p=A.K(p<10?48+p:87+p)
t.a+=p}}continue}if(q<32){if(r>s)t.a+=B.m.X(a,s,r)
s=r+1
p=A.K(92)
t.a+=p
switch(q){case 8:p=A.K(98)
t.a+=p
break
case 9:p=A.K(116)
t.a+=p
break
case 10:p=A.K(110)
t.a+=p
break
case 12:p=A.K(102)
t.a+=p
break
case 13:p=A.K(114)
t.a+=p
break
default:p=A.K(117)
t.a+=p
p=A.K(48)
t.a=(t.a+=p)+p
p=q>>>4&15
p=A.K(p<10?48+p:87+p)
t.a+=p
p=q&15
p=A.K(p<10?48+p:87+p)
t.a+=p
break}}else if(q===34||q===92){if(r>s)t.a+=B.m.X(a,s,r)
s=r+1
p=A.K(92)
t.a+=p
p=A.K(q)
t.a+=p}}if(s===0)t.a+=a
else if(s<n)t.a+=B.m.X(a,s,n)},
a9(a){var t,s,r,q
for(t=this.a,s=t.length,r=0;r<s;++r){q=t[r]
if(a==null?q==null:a===q)throw A.a(new A.c9(a,null))}B.a.l(t,a)},
a7(a){var t,s,r,q,p=this
if(p.aR(a))return
p.a9(a)
try{t=p.b.$1(a)
if(!p.aR(t)){r=A.em(a,null,p.gaF())
throw A.a(r)}r=p.a
if(0>=r.length)return A.d(r,-1)
r.pop()}catch(q){s=A.e8(q)
r=A.em(a,s,p.gaF())
throw A.a(r)}},
aR(a){var t,s,r=this
if(typeof a=="number"){if(!isFinite(a))return!1
r.c.a+=B.c.k(a)
return!0}else if(a===!0){r.c.a+="true"
return!0}else if(a===!1){r.c.a+="false"
return!0}else if(a==null){r.c.a+="null"
return!0}else if(typeof a=="string"){t=r.c
t.a+='"'
r.aS(a)
t.a+='"'
return!0}else if(u.j.b(a)){r.a9(a)
r.bD(a)
t=r.a
if(0>=t.length)return A.d(t,-1)
t.pop()
return!0}else if(u.f.b(a)){r.a9(a)
s=r.bE(a)
t=r.a
if(0>=t.length)return A.d(t,-1)
t.pop()
return s}else return!1},
bD(a){var t,s,r=this.c
r.a+="["
t=J.U(a)
if(t.gJ(a)){this.a7(t.h(a,0))
for(s=1;s<t.gj(a);++s){r.a+=","
this.a7(t.h(a,s))}}r.a+="]"},
bE(a){var t,s,r,q,p,o,n=this,m={}
if(a.gt(a)){n.c.a+="{}"
return!0}t=a.gj(a)*2
s=A.cI(t,null,!1,u.X)
r=m.a=0
m.b=!0
a.N(0,new A.d6(m,s))
if(!m.b)return!1
q=n.c
q.a+="{"
for(p='"';r<t;r+=2,p=',"'){q.a+=p
n.aS(A.L(s[r]))
q.a+='":'
o=r+1
if(!(o<t))return A.d(s,o)
n.a7(s[o])}q.a+="}"
return!0}}
A.d6.prototype={
$2(a,b){var t,s
if(typeof a!="string")this.a.b=!1
t=this.b
s=this.a
B.a.A(t,s.a++,a)
B.a.A(t,s.a++,b)},
$S:3}
A.d4.prototype={
gaF(){var t=this.c.a
return t.charCodeAt(0)==0?t:t}}
A.cm.prototype={
bo(a){var t,s,r,q,p=a.length,o=A.cM(0,null,p)
if(o===0)return new Uint8Array(0)
t=o*3
s=new Uint8Array(t)
r=new A.da(s)
if(r.b3(a,0,o)!==o){q=o-1
if(!(q>=0&&q<p))return A.d(a,q)
r.ah()}return new Uint8Array(s.subarray(0,A.hp(0,r.b,t)))}}
A.da.prototype={
ah(){var t,s=this,r=s.c,q=s.b,p=s.b=q+1
r.$flags&2&&A.M(r)
t=r.length
if(!(q<t))return A.d(r,q)
r[q]=239
q=s.b=p+1
if(!(p<t))return A.d(r,p)
r[p]=191
s.b=q+1
if(!(q<t))return A.d(r,q)
r[q]=189},
bh(a,b){var t,s,r,q,p,o=this
if((b&64512)===56320){t=65536+((a&1023)<<10)|b&1023
s=o.c
r=o.b
q=o.b=r+1
s.$flags&2&&A.M(s)
p=s.length
if(!(r<p))return A.d(s,r)
s[r]=t>>>18|240
r=o.b=q+1
if(!(q<p))return A.d(s,q)
s[q]=t>>>12&63|128
q=o.b=r+1
if(!(r<p))return A.d(s,r)
s[r]=t>>>6&63|128
o.b=q+1
if(!(q<p))return A.d(s,q)
s[q]=t&63|128
return!0}else{o.ah()
return!1}},
b3(a,b,c){var t,s,r,q,p,o,n,m,l=this
if(b!==c){t=c-1
if(!(t>=0&&t<a.length))return A.d(a,t)
t=(a.charCodeAt(t)&64512)===55296}else t=!1
if(t)--c
for(t=l.c,s=t.$flags|0,r=t.length,q=a.length,p=b;p<c;++p){if(!(p<q))return A.d(a,p)
o=a.charCodeAt(p)
if(o<=127){n=l.b
if(n>=r)break
l.b=n+1
s&2&&A.M(t)
t[n]=o}else{n=o&64512
if(n===55296){if(l.b+4>r)break
n=p+1
if(!(n<q))return A.d(a,n)
if(l.bh(o,a.charCodeAt(n)))p=n}else if(n===56320){if(l.b+3>r)break
l.ah()}else if(o<=2047){n=l.b
m=n+1
if(m>=r)break
l.b=m
s&2&&A.M(t)
if(!(n<r))return A.d(t,n)
t[n]=o>>>6|192
l.b=m+1
t[m]=o&63|128}else{n=l.b
if(n+2>=r)break
m=l.b=n+1
s&2&&A.M(t)
if(!(n<r))return A.d(t,n)
t[n]=o>>>12|224
n=l.b=m+1
if(!(m<r))return A.d(t,m)
t[m]=o>>>6&63|128
l.b=n+1
if(!(n<r))return A.d(t,n)
t[n]=o&63|128}}}return p}}
A.cn.prototype={
k(a){return this.a_()},
$ibZ:1}
A.u.prototype={}
A.bR.prototype={
k(a){var t=this.a
if(t!=null)return"Assertion failed: "+A.c_(t)
return"Assertion failed"}}
A.by.prototype={}
A.a3.prototype={
gac(){return"Invalid argument"+(!this.a?"(s)":"")},
gab(){return""},
k(a){var t=this,s=t.c,r=s==null?"":" ("+s+")",q=t.d,p=q==null?"":": "+A.l(q),o=t.gac()+r+p
if(!t.a)return o
return o+t.gab()+": "+A.c_(t.gal())},
gal(){return this.b}}
A.bs.prototype={
gal(){return A.aq(this.b)},
gac(){return"RangeError"},
gab(){var t,s=this.e,r=this.f
if(s==null)t=r!=null?": Not less than or equal to "+A.l(r):""
else if(r==null)t=": Not greater than or equal to "+A.l(s)
else if(r>s)t=": Not in inclusive range "+A.l(s)+".."+A.l(r)
else t=r<s?": Valid value range is empty":": Only valid value is "+A.l(s)
return t}}
A.c1.prototype={
gal(){return A.F(this.b)},
gac(){return"RangeError"},
gab(){if(A.F(this.b)<0)return": index must not be negative"
var t=this.f
if(t===0)return": no indices are valid"
return": index should be less than "+t},
gj(a){return this.f}}
A.bz.prototype={
k(a){return"Unsupported operation: "+this.a}}
A.ck.prototype={
k(a){return"UnimplementedError: "+this.a}}
A.aZ.prototype={
k(a){return"Bad state: "+this.a}}
A.bV.prototype={
k(a){var t=this.a
if(t==null)return"Concurrent modification during iteration."
return"Concurrent modification during iteration: "+A.c_(t)+"."}}
A.bw.prototype={
k(a){return"Stack Overflow"},
$iu:1}
A.d2.prototype={
k(a){return"Exception: "+this.a}}
A.cE.prototype={
k(a){var t=this.a,s=""!==t?"FormatException: "+t:"FormatException"
return s}}
A.b.prototype={
a2(a,b){return A.dL(this,A.h(this).i("b.E"),b)},
U(a,b,c){var t=A.h(this)
return A.fI(this,t.q(c).i("1(b.E)").a(b),t.i("b.E"),c)},
B(a,b){var t
for(t=this.gp(this);t.m();)if(J.v(t.gn(),b))return!0
return!1},
P(a,b){var t=A.h(this).i("b.E")
if(b)t=A.aC(this,t)
else{t=A.aC(this,t)
t.$flags=1
t=t}return t},
a6(a){return this.P(0,!0)},
H(a){return A.eo(this,A.h(this).i("b.E"))},
gj(a){var t,s=this.gp(this)
for(t=0;s.m();)++t
return t},
gt(a){return!this.gp(this).m()},
gJ(a){return!this.gt(this)},
L(a,b){return A.et(this,b,A.h(this).i("b.E"))},
gE(a){var t=this.gp(this)
if(!t.m())throw A.a(A.C())
return t.gn()},
gF(a){var t,s=this.gp(this)
if(!s.m())throw A.a(A.C())
do t=s.gn()
while(s.m())
return t},
ai(a,b){var t,s
A.h(this).i("a7(b.E)").a(b)
for(t=this.gp(this);t.m();){s=t.gn()
if(b.$1(s))return s}throw A.a(A.C())},
u(a,b){var t,s
A.V(b,"index")
t=this.gp(this)
for(s=b;t.m();){if(s===0)return t.gn();--s}throw A.a(A.c2(b,b-s,this,null,"index"))},
k(a){return A.fB(this,"(",")")}}
A.bp.prototype={
gv(a){return A.m.prototype.gv.call(this,0)},
k(a){return"null"}}
A.m.prototype={$im:1,
R(a,b){return this===b},
gv(a){return A.br(this)},
k(a){return"Instance of '"+A.cf(this)+"'"},
gG(a){return A.i4(this)},
toString(){return this.k(this)}}
A.b_.prototype={
gj(a){return this.a.length},
k(a){var t=this.a
return t.charCodeAt(0)==0?t:t},
$ifR:1}
A.bY.prototype={}
A.aR.prototype={
R(a,b){var t,s,r,q,p,o,n
if(b==null)return!1
if(b instanceof A.aR){t=this.a
s=b.a
r=t.length
q=s.length
if(r!==q)return!1
for(p=0,o=0;o<r;++o){n=t[o]
if(!(o<q))return A.d(s,o)
p|=n^s[o]}return p===0}return!1},
gv(a){return A.fM(this.a)},
k(a){return A.eP(this.a)}}
A.bW.prototype={$ibu:1}
A.c0.prototype={
ap(a){var t,s,r,q,p,o,n,m,l,k,j,i=this
u.I.a(a)
t=i.e
s=i.d
r=s.length
if(i.c==null)i.c=J.dI(B.k.gW(s))
for(q=i.f,p=q.$flags|0,o=q.length,n=a.length,m=0;;t=0){l=t+n-m
if(l<r){B.k.T(s,t,l,a,m)
i.e=l
return}B.k.T(s,t,r,a,m)
m+=r-t
k=0
do{j=i.c.getUint32(k*4,!1)
p&2&&A.M(q)
if(!(k<o))return A.d(q,k)
q[k]=j;++k}while(k<o)
i.bC(q)}},
bm(){var t,s,r,q,p,o,n,m=this
if(m.w)return
m.w=!0
t=m.r
if(t>1125899906842623)A.i(A.b1("Hashing is unsupported for messages with more than 2^53 bits."))
s=m.d.byteLength
s=((t+1+8+s-1&-s)>>>0)-t
r=new Uint8Array(s)
if(0>=s)return A.d(r,0)
r[0]=128
q=t*8
p=s-8
o=J.dI(B.k.gW(r))
n=B.f.bf(q,4294967296)
o.$flags&2&&A.M(o,11)
o.setUint32(p,n,!1)
o.setUint32(p+4,q>>>0,!1)
m.ap(r)
t=m.a
s=m.aZ()
if(t.a!=null)A.i(A.af("add may only be called once."))
t.a=new A.aR(s)},
aZ(){var t,s,r,q,p,o,n
if(B.G===$.f6())return J.fl(B.ak.gW(this.y))
t=this.y
s=t.byteLength
r=new Uint8Array(s)
q=J.dI(B.k.gW(r))
for(s=t.length,p=q.$flags|0,o=0;o<s;++o){n=t[o]
p&2&&A.M(q,11)
q.setUint32(o*4,n,!1)}return r},
$ibu:1}
A.cu.prototype={
bC(a){var t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b
for(t=this.z,s=a.length,r=t.$flags|0,q=0;q<16;++q){if(!(q<s))return A.d(a,q)
p=a[q]
r&2&&A.M(t)
t[q]=p}for(q=16;q<64;++q){s=t[q-2]
p=t[q-7]
o=t[q-15]
n=t[q-16]
r&2&&A.M(t)
t[q]=((((s>>>17|s<<15)^(s>>>19|s<<13)^s>>>10)>>>0)+p>>>0)+((((o>>>7|o<<25)^(o>>>18|o<<14)^o>>>3)>>>0)+n>>>0)>>>0}s=this.y
r=s.length
if(0>=r)return A.d(s,0)
m=s[0]
if(1>=r)return A.d(s,1)
l=s[1]
if(2>=r)return A.d(s,2)
k=s[2]
if(3>=r)return A.d(s,3)
j=s[3]
if(4>=r)return A.d(s,4)
i=s[4]
if(5>=r)return A.d(s,5)
h=s[5]
if(6>=r)return A.d(s,6)
g=s[6]
if(7>=r)return A.d(s,7)
f=s[7]
for(e=m,q=0;q<64;++q,f=g,g=h,h=i,i=c,j=k,k=l,l=e,e=b){d=(f+(((i>>>6|i<<26)^(i>>>11|i<<21)^(i>>>25|i<<7))>>>0)>>>0)+(((i&h^~i&g)>>>0)+(B.a9[q]+t[q]>>>0)>>>0)>>>0
c=j+d>>>0
b=d+((((e>>>2|e<<30)^(e>>>13|e<<19)^(e>>>22|e<<10))>>>0)+((e&l^e&k^l&k)>>>0)>>>0)>>>0}s.$flags&2&&A.M(s)
s[0]=e+m>>>0
s[1]=l+s[1]>>>0
s[2]=k+s[2]>>>0
s[3]=j+s[3]>>>0
s[4]=i+s[4]>>>0
s[5]=h+s[5]>>>0
s[6]=g+s[6]>>>0
s[7]=f+s[7]>>>0}}
A.ct.prototype={}
A.p.prototype={
a_(){return"Light."+this.b}}
A.dH.prototype={
$2(a,b){var t=u.R
t.a(a)
t.a(b)
return b.a>a.a?b:a},
$S:8}
A.O.prototype={
a_(){return"ActionKind."+this.b}}
A.a4.prototype={
a_(){return"EmState."+this.b}}
A.Y.prototype={
a_(){return"EmAction."+this.b}}
A.bX.prototype={
aG(a,b){this.d=B.v
this.e=a+A.j(this.a.h(0,"call_119_confirm_timeout_seconds"))
return A.t([new A.r(B.Z,b)],u._)},
Y(a){var t
if(a<this.c)throw A.a(A.X("time went backwards"))
this.c=a
t=this.d
t===$&&A.a1()
return!B.aF.B(0,t)},
bi(a,b){var t,s=this
if(s.Y(a)){t=s.d
t===$&&A.a1()
t=t!==B.l}else t=!0
if(t)return B.j
if(b){s.d=B.K
return B.ab}s.d=B.u
return B.ad},
bz(a){var t
if(this.Y(a)){t=this.d
t===$&&A.a1()
t=t!==B.l}else t=!0
if(t)return B.j
return this.aG(a,"EM_SEVERE_SYMPTOM")},
bn(a){var t
if(this.Y(a)){t=this.d
t===$&&A.a1()
t=t!==B.v}else t=!0
if(t)return B.j
this.d=B.L
return B.aa},
an(a){var t,s=this
if(s.Y(a)){t=s.e
t===$&&A.a1()
t=a<t}else t=!0
if(t)return B.j
t=s.d
t===$&&A.a1()
if(t===B.l){s.d=B.u
return B.ac}if(t===B.v){s.d=B.M
return B.a8}return B.j}}
A.cC.prototype={
bk(a){var t,s=this
A:{if("systolic_max"===a){t=s.a
break A}if("diastolic_max"===a){t=s.b
break A}if("resting_hr_max"===a){t=s.c
break A}t=s.d
break A}return t}}
A.cL.prototype={}
A.d1.prototype={}
A.cB.prototype={}
A.dm.prototype={
$1(a){return J.aj(a)},
$S:4}
A.dl.prototype={
$1(a){var t=J.A(a)
if(t.h(a,"lower")==null||this.a>=A.j(t.h(a,"lower")))t=t.h(a,"upper")==null||this.a<A.j(t.h(a,"upper"))
else t=!1
return t},
$S:9}
A.dF.prototype={
$2(a,b){var t
u.Q.a(a)
t=J.bP(u.j.a(J.f(this.a,b)),u.N)
return a.ak(t.H(t)).a!==0},
$S:10}
A.dG.prototype={
$1(a){return u.d.a(a).a},
$S:11}
A.cO.prototype={
k(a){return"RuleError: "+this.a}}
A.dt.prototype={
$1(a){return J.aj(a)},
$S:4}
A.du.prototype={
$1(a){A.L(a)
return B.b.D(a,null)+":"+A.e1(this.a.h(0,a))},
$S:5}
A.cN.prototype={
h(a,b){var t=this.a
return t.$ti.i("4?").a(t.a.h(0,b))}}
A.I.prototype={
k(a){return"["+A.l(this.a)+", "+this.b.b+", "+this.c+"]"}}
A.ch.prototype={
an(a){return this.ba(a,"tick",null,new A.cX())},
bu(a,b){return this.bb(a,"hr",b,new A.cR(this,a,b),!0)},
bw(a,b){var t=this.a.h(0,"rpe"),s=A.j(typeof b=="string"?J.f(J.f(t,"answer_map"),b):A.j(b)),r=J.A(t),q=J.f(r.h(t,"valid"),"min")
if(typeof q!=="number")return q.S()
if(!(q<=s&&s<=A.j(J.f(r.h(t,"valid"),"max"))))A.i(A.X("RPE out of range: "+A.l(b)))
return this.V(a,"rpe",b,new A.cT(this,a,s),!0)},
bx(a,b){var t,s,r={}
r.a=r.b=null
t=this.a
s=u.j
if(J.bQ(s.a(t.h(0,"emergency_symptoms")),b)){r.b=B.A
r.a="EMERGENCY_SYMPTOM"}else if(J.bQ(s.a(t.h(0,"stop_symptoms")),b)){r.b=B.e
r.a="STOP_SYMPTOM"}else throw A.a(A.X("unknown symptom: "+b))
return this.V(a,"symptom",b,new A.cU(r,this,a,b),!0)},
by(a){return this.V(a,"user_stop",null,new A.cV(this,a),!0)},
bv(a){return this.V(a,"interaction",null,new A.cS(),!0)},
bA(a){return this.V(a,"resume",null,new A.cW(this,a),!0)},
ag(a,b,c,d,e,f){var t,s,r,q=this,p="NO_RESPONSE"
u.bU.a(d)
t=q.w
if(a<t)throw A.a(A.X("time went backwards: "+A.l(a)+" < "+A.l(t)))
q.w=a
if(q.x)return B.ae
s=A.t([],u.v)
if(f){q.ay=a
q.ch=!1}if(e)q.ar(a,s)
d.$1(s)
if(!q.x){u.w.a(s)
q.ar(a,s)
if(!q.y&&q.Q!=null){if(q.as==null){t=q.Q
t.toString
t=a-t>A.j(q.a.h(0,"over_ceiling_seconds_to_slow_down"))}else t=!1
if(t){q.as=a
B.a.l(s,new A.I(a,B.z,"HR_OVER_CEILING",A.w(["ceiling",q.b],u.N,u.z)))}else{t=q.as
if(t!=null&&a-t>=A.j(q.a.h(0,"recover_seconds_after_slow_down"))){q.y=!0
B.a.l(s,new A.I(a,B.q,"HR_NOT_RECOVERED",A.w(["ceiling",q.b],u.N,u.z)))}}}if(!q.y){t=q.ax
r=q.f
r===$&&A.a1()
r=a-t>=r
t=r}else t=!1
if(t){q.ax=a
B.a.l(s,new A.I(a,B.B,"CHECKIN_DUE",B.d))}if(!q.ch&&a-q.ay>=A.j(q.a.h(0,"no_response_seconds"))){q.ch=!0
B.a.l(s,new A.I(a,B.C,p,B.d))
B.a.l(s,new A.I(a,B.D,p,B.d))}}return s},
V(a,b,c,d,e){return this.ag(a,b,c,d,!1,e)},
bb(a,b,c,d,e){return this.ag(a,b,c,d,e,!1)},
ba(a,b,c,d){return this.ag(a,b,c,d,!1,!1)},
a0(a,b,c,d,e){u.w.a(d)
u.P.a(e)
this.x=!0
B.a.l(d,new A.I(a,b,c,e))},
be(a,b,c,d){return this.a0(a,b,c,d,B.d)},
aD(a,b,c,d){var t=this
u.w.a(c)
u.P.a(d)
if(t.d===B.e)t.a0(a,B.e,b,c,d)
else if(!t.y){t.y=!0
B.a.l(c,new A.I(a,B.q,b,d))}},
az(a,b,c){var t=this
u.w.a(c)
if(t.z)return
t.z=!0
t.f=A.F(J.f(t.a.h(0,"sensor"),"fallback_checkin_interval_seconds"))
t.as=t.Q=null
B.a.l(c,new A.I(a,B.E,b,B.d))
B.a.l(c,new A.I(a,B.p,b,B.d))},
ar(a,b){var t,s=this
u.w.a(b)
t=s.c
t===$&&A.a1()
if(t&&!s.z&&a-s.at>A.j(J.f(s.a.h(0,"sensor"),"hr_gap_seconds")))s.az(a,"SENSOR_GAP",b)},
b5(a,b,c){var t,s,r,q,p,o,n,m,l,k,j,i,h,g=this
u.w.a(c)
t=g.c
t===$&&A.a1()
if(!t)return
t=g.a
s=J.f(t.h(0,"sensor"),"plausible")
r=J.A(s)
q=r.h(s,"min")
if(typeof q!=="number")return q.S()
if(!(q<=b&&b<=A.j(r.h(s,"max")))){g.az(a,"SENSOR_IMPLAUSIBLE",c)
return}g.at=a
if(g.z){g.z=!1
r=g.e
r===$&&A.a1()
g.f=r
B.a.l(c,new A.I(a,B.F,"SENSOR_OK",B.d))}p=t.h(0,"sudden_change")
r=g.CW
q=J.A(p)
o=r.$ti
n=o.c
for(;;){if(!r.gt(0)){m=r.b
if(m===r.c)A.i(A.C())
l=r.a
if(!(m<l.length))return A.d(l,m)
m=l[m]
m=a-(m==null?n.a(m):m).a>A.j(q.h(p,"window_seconds"))}else m=!1
if(!m)break
m=r.b
if(m===r.c)A.i(A.C());++r.d
l=r.a
if(!(m<l.length))return A.d(l,m)
k=l[m]
if(k==null)n.a(k)
B.a.A(l,m,null)
r.b=(r.b+1&r.a.length-1)>>>0}j=r.aO(0,0,new A.cQ(b),u.H)
n=n.a(new A.r(a,b))
B.a.A(r.a,r.c,n)
n=r.c
m=r.a.length
n=(n+1&m-1)>>>0
r.c=n
if(r.b===n){i=A.cI(m*2,null,!1,o.i("1?"))
o=r.a
n=r.b
h=o.length-n
B.a.T(i,0,h,o,n)
B.a.T(i,h,h+r.b,r.a,0)
r.b=0
r.c=r.a.length
r.a=i}++r.d
r=g.b
if(b>=B.c.a5(r*A.j(t.h(0,"stop_ratio_over_ceiling"))*1e6)/1e6)g.aD(a,"HR_FAR_OVER_CEILING",c,A.w(["bpm",b,"ceiling",r],u.N,u.z))
else if(j>=A.j(q.h(p,"delta_bpm")))g.aD(a,"HR_SUDDEN_CHANGE",c,A.w(["bpm",b,"jump",j],u.N,u.z))
if(g.x)return
if(b>r){if(g.Q==null)g.Q=a}else g.as=g.Q=null}}
A.cX.prototype={
$1(a){u.w.a(a)},
$S:1}
A.cR.prototype={
$1(a){return this.a.b5(this.b,this.c,u.w.a(a))},
$S:1}
A.cT.prototype={
$1(a){var t,s,r,q
u.w.a(a)
t=this.a
s=t.ax=this.b
r=this.c
q=t.a
if(r>=A.j(J.f(q.h(0,"rpe"),"stop_at")))t.a0(s,B.e,"RPE_VERY_HARD",a,A.w(["rpe",r],u.N,u.z))
else if(r>=A.j(J.f(q.h(0,"rpe"),"step_down_at")))B.a.l(a,new A.I(s,B.p,"RPE_HARD",A.w(["rpe",r],u.N,u.z)))},
$S:1}
A.cU.prototype={
$1(a){var t,s=this
u.w.a(a)
t=s.a
return s.b.a0(s.c,t.b,t.a,a,A.w(["symptom",s.d],u.N,u.z))},
$S:1}
A.cV.prototype={
$1(a){return this.a.be(this.b,B.e,"USER_STOP",u.w.a(a))},
$S:1}
A.cS.prototype={
$1(a){u.w.a(a)},
$S:1}
A.cW.prototype={
$1(a){var t
u.w.a(a)
t=this.a
t.y=!1
t.as=t.Q=null
t.ax=this.b},
$S:1}
A.cQ.prototype={
$2(a,b){return Math.max(A.j(a),Math.abs(this.a-u.D.a(b).b))},
$S:12}
A.dc.prototype={
$1(a){var t,s,r,q,p,o,n=u.N,m=u.z,l=u.f.a(u.P.a(a).h(0,"bundle")).a3(0,n,m)
A.im(l)
t=u.I.a(B.X.bo(A.e1(l)))
s=new A.bW()
u.h.a(s)
r=new Uint32Array(A.eL(A.t([1779033703,3144134277,1013904242,2773480762,1359893119,2600822924,528734635,1541459225],u.t)))
q=new Uint32Array(64)
p=new Uint8Array(64)
r=new A.ct(r,q,s,p,new Uint32Array(16))
r.r=t.length
r.ap(t)
r.bm()
o=A.eP(s.a.a)
t=J.aj(J.f(l.$ti.i("4?").a(l.a.h(0,"meta")),"version"))
$.b4=new A.cN(l,t,o)
return B.b.D(A.w(["version",t,"status",J.f(l.$ti.i("4?").a(l.a.h(0,"meta")),"status")],n,m),null)},
$S:0}
A.dd.prototype={
$1(a){var t,s,r,q,p,o,n,m,l,k,j,i
u.P.a(a)
t=u.f
s=t.a(a.h(0,"vitals"))
r=$.b4
if(r==null)r=A.i(A.af("load() first"))
t=A.eV(t.a(a.h(0,"profile")))
q=A.aq(s.h(0,"systolic"))
p=A.aq(s.h(0,"diastolic"))
o=A.aq(s.h(0,"resting_hr"))
n=A.b3(s.h(0,"bp_source"))
if(n==null)n="manual"
m=A.b3(s.h(0,"hr_source"))
if(m==null)m="manual"
l=u.g
k=l.a(a.h(0,"symptoms"))
if(k==null)k=B.x
j=u.N
k=J.bP(k,j)
l=l.a(a.h(0,"conditions"))
i=A.ig(r,t,new A.d1(q,p,o,n,m),J.bP(l==null?B.x:l,j),k)
return B.b.D(A.w(["outcome",i.b,"reasons",i.c,"rule_version",i.d,"detail",i.f],j,u.K),null)},
$S:0}
A.de.prototype={
$1(a){var t
u.P.a(a)
t=$.b4
if(t==null)t=A.i(A.af("load() first"))
return B.b.D(A.hU(t,A.cD(B.w,A.L(a.h(0,"light")),u.R),A.F(a.h(0,"minutes"))),null)},
$S:0}
A.df.prototype={
$1(a){var t,s,r,q,p
u.P.a(a)
t=$.b4
if(t==null)t=A.i(A.af("load() first"))
s=A.j(a.h(0,"resting_hr"))
r=t.a
q=A.j(a.h(0,"hr_after_recovery"))-s>=A.j(J.f(r.$ti.i("4?").a(r.a.h(0,"post")),"elevated_delta_bpm"))
s=q?"SLOW_RECOVERY":"RECOVERED"
r=u.N
p=A.dr(t,"post_check",s,A.t([q?"POST_SLOW_RECOVERY":"POST_RECOVERED"],u.s),A.w(["next_intensity_down",q],r,u.z))
return B.b.D(A.w(["outcome",p.b,"reasons",p.c],r,u.K),null)},
$S:0}
A.dg.prototype={
$1(a){var t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c="absolute_max"
u.P.a(a)
t=$.b4
if(t==null)t=A.i(A.af("load() first"))
s=u.f
r=A.eV(s.a(a.h(0,"profile")))
q=A.eK(a.h(0,"weeks"))
if(q==null)q=0
p=J.v(a.h(0,"escalation"),!0)
o=A.b3(a.h(0,"light"))
if(o==null)o="GREEN"
o=A.cD(B.w,o,u.R)
t=t.a
n=t.a
t=t.$ti.i("4?")
m=t.a(n.h(0,"session"))
l=J.A(m)
k=l.h(m,"ceiling_pct")
j=A.j(J.f(l.h(m,"max_hr"),"intercept"))-A.j(J.f(l.h(m,"max_hr"),"age_coef"))*r.a
if(r.e){i=A.j(J.f(k,c))
h="anomaly_only"}else{q=q>=A.j(l.h(m,"initial_period_weeks"))&&p
p=J.A(k)
i=q?A.j(p.h(k,"escalated")):A.j(p.h(k,"initial"))
h="zone"}i=Math.min(i,A.j(J.f(k,c)))
s=s.a(t.a(n.h(0,"allowance"))).h(0,o.b)
g=s==null?null:J.f(s,"hr_ceiling_pct_cap")
if(g!=null)i=Math.min(i,A.j(g))
f=B.c.aN(B.c.a5(j*i*1e6)/1e6)
e=r.r.d
if(e!=null)f=Math.min(f,B.c.aQ(e))
else if(J.bQ(u.j.a(J.f(t.a(n.h(0,"hard_gate")),"devices_requiring_doctor_hr_ceiling")),r.f))A.i(A.X("pacemaker/ICD user without doctor HR ceiling must be blocked by the hard gate"))
d=h==="anomaly_only"?null:Math.min(B.c.bl(B.c.a5(j*A.j(J.f(l.h(m,"zone_pct"),"lower"))*1e6)/1e6),f)
return B.b.D(A.w(["max_hr",B.c.a5(j*10)/10,"ceiling_pct",i,"ceiling",f,"zone_lower",d,"mode",h],u.N,u.X),null)},
$S:0}
A.dh.prototype={
$1(a){var t,s,r,q,p,o,n=null
u.P.a(a)
t=$.ds
$.ds=t+1
s=$.b4
if(s==null)s=A.i(A.af("load() first"))
r=A.F(a.h(0,"ceiling"))
q=A.b3(a.h(0,"hr_grade"))
p=A.cI(A.fG(n),n,!1,u.cl)
s=s.a
s=u.f.a(s.$ti.i("4?").a(s.a.h(0,"session")))
p=new A.ch(s,r,new A.bj(p,u.A))
o=q==null?n:J.f(s.h(0,"heart_rate_grades"),q)
r=o!=null&&J.v(J.f(o,"use_hr"),!0)
p.c=r
p.d=r?A.cD(B.af,A.L(J.f(o,"max_hr_action")),u.k):n
p.f=p.e=A.F(r?s.h(0,"checkin_interval_seconds"):s.h(0,"no_sensor_checkin_interval_seconds"))
$.eU.A(0,t,p)
return B.b.D(A.w(["id",t],u.N,u.S),n)},
$S:0}
A.di.prototype={
$1(a){var t,s,r,q,p
u.P.a(a)
t=$.eU.h(0,A.F(a.h(0,"id")))
t.toString
s=A.j(a.h(0,"t"))
r=a.h(0,"value")
q=A.L(a.h(0,"event"))
A:{if("tick"===q){p=t.an(s)
break A}if("hr"===q){p=t.bu(s,A.j(r))
break A}if("rpe"===q){p=t.bw(s,r==null?A.dX(r):r)
break A}if("symptom"===q){p=t.bx(s,A.L(r))
break A}if("user_stop"===q){p=t.by(s)
break A}if("interaction"===q){p=t.bv(s)
break A}if("resume"===q){p=t.bA(s)
break A}p=A.i(A.X("unknown event "+q))}return B.b.D(A.w(["actions",A.hd(p),"stopped",t.x,"paused",t.y],u.N,u.K),null)},
$S:0}
A.dj.prototype={
$1(a){var t,s,r,q,p
u.P.a(a)
t=$.ds
$.ds=t+1
s=$.b4
if(s==null)s=A.i(A.af("load() first"))
r=A.j(a.h(0,"t"))
q=J.v(a.h(0,"severe"),!0)
s=s.a
s=u.f.a(s.$ti.i("4?").a(s.a.h(0,"emergency")))
p=new A.bX(s,r)
if(q)s=p.aG(r,"EM_SEVERE_SYMPTOM")
else{p.d=B.l
p.e=r+A.j(s.h(0,"ask_ok_timeout_seconds"))
s=B.ag}u.u.a(s)
p.f!==$&&A.ik()
p.f=s
$.eN.A(0,t,p)
s=A.eX(s)
r=p.d
r===$&&A.a1()
return B.b.D(A.w(["id",t,"actions",s,"state",r.b],u.N,u.K),null)},
$S:0}
A.dk.prototype={
$1(a){var t,s,r,q
u.P.a(a)
t=$.eN.h(0,A.F(a.h(0,"id")))
t.toString
s=A.j(a.h(0,"t"))
r=A.L(a.h(0,"op"))
A:{if("answer"===r){q=t.bi(s,J.v(a.h(0,"ok"),!0))
break A}if("report_severe"===r){q=t.bz(s)
break A}if("confirm_119"===r){q=t.bn(s)
break A}if("tick"===r){q=t.an(s)
break A}q=A.i(A.X("unknown op "+r))}q=A.eX(q)
t=t.d
t===$&&A.a1()
return B.b.D(A.w(["actions",q,"state",t.b],u.N,u.K),null)},
$S:0}
A.dD.prototype={
$2(a,b){var t,s
A.L(a)
t=new A.dC(u.V.a(b))
if(typeof t=="function")A.i(A.X("Attempting to rewrap a JS function."))
s=function(c,d){return function(e){return c(d,e,arguments.length)}}(A.hn,t)
s[$.e9()]=t
this.a[a]=s},
$S:13}
A.dC.prototype={
$1(a){return A.hm(this.a,A.L(a))},
$S:5};(function aliases(){var t=J.am.prototype
t.aV=t.k
t=A.x.prototype
t.aW=t.T})();(function installTearOffs(){var t=hunkHelpers._static_2,s=hunkHelpers._static_1
t(J,"hz","fD",14)
s(A,"hZ","hq",2)
s(A,"ii","e1",15)})();(function inheritance(){var t=hunkHelpers.mixin,s=hunkHelpers.inherit,r=hunkHelpers.inheritMany
s(A.m,null)
r(A.m,[A.dM,J.c3,A.bt,J.as,A.b,A.b8,A.z,A.ak,A.u,A.cP,A.aB,A.bk,A.bv,A.bb,A.ay,A.ao,A.b9,A.ai,A.ad,A.d_,A.cK,A.cH,A.bi,A.d9,A.Z,A.cp,A.cv,A.cs,A.aG,A.x,A.bD,A.bU,A.aQ,A.d5,A.da,A.cn,A.bw,A.d2,A.cE,A.bp,A.b_,A.bY,A.aR,A.bW,A.c0,A.bX,A.cC,A.cL,A.d1,A.cB,A.cO,A.cN,A.I,A.ch])
r(J.c3,[J.c5,J.be,J.bf,J.aV,J.aX,J.aU,J.az])
r(J.bf,[J.am,J.o,A.aE,A.bl])
r(J.am,[J.ce,J.b0,J.a9])
s(J.c4,A.bt)
s(J.cG,J.o)
r(J.aU,[J.bd,J.c6])
r(A.b,[A.an,A.k,A.aD,A.ae,A.bC])
r(A.an,[A.at,A.bM])
s(A.bB,A.at)
s(A.bA,A.bM)
s(A.a8,A.bA)
r(A.z,[A.au,A.aa,A.cq])
r(A.ak,[A.bT,A.cj,A.dy,A.dA,A.dm,A.dl,A.dG,A.dt,A.du,A.cX,A.cR,A.cT,A.cU,A.cV,A.cS,A.cW,A.dc,A.dd,A.de,A.df,A.dg,A.dh,A.di,A.dj,A.dk,A.dC])
r(A.bT,[A.cA,A.dz,A.cJ,A.d6,A.dH,A.dF,A.cQ,A.dD])
r(A.u,[A.aY,A.by,A.c7,A.cl,A.cg,A.co,A.bh,A.bR,A.a3,A.bz,A.ck,A.aZ,A.bV])
r(A.k,[A.D,A.ax,A.aA])
r(A.D,[A.bx,A.R,A.bj,A.cr])
s(A.aw,A.aD)
s(A.aS,A.ae)
s(A.b2,A.ao)
s(A.r,A.b2)
s(A.av,A.b9)
r(A.ad,[A.aP,A.bG])
r(A.aP,[A.ba,A.bc])
s(A.bq,A.by)
r(A.cj,[A.ci,A.aO])
s(A.bg,A.aa)
r(A.bl,[A.cd,A.a5])
s(A.bE,A.a5)
s(A.bF,A.bE)
s(A.ab,A.bF)
r(A.ab,[A.bm,A.bn,A.bo])
s(A.bH,A.co)
s(A.aF,A.bG)
s(A.c9,A.bh)
s(A.c8,A.bU)
r(A.aQ,[A.cb,A.ca,A.cm])
s(A.d4,A.d5)
r(A.a3,[A.bs,A.c1])
s(A.cu,A.c0)
s(A.ct,A.cu)
r(A.cn,[A.p,A.O,A.a4,A.Y])
t(A.bM,A.x)
t(A.bE,A.x)
t(A.bF,A.ay)})()
var v={G:typeof self!="undefined"?self:globalThis,typeUniverse:{eC:new Map(),tR:{},eT:{},tPV:{},sEA:[]},mangledGlobalNames:{e:"int",f_:"double",q:"num",c:"String",a7:"bool",bp:"Null",n:"List",m:"Object",J:"Map",Q:"JSObject"},mangledNames:{},types:["c(J<c,@>)","~(n<I>)","@(@)","~(m?,m?)","c(@)","c(c)","@(@,c)","@(c)","p(p,p)","a7(@)","a7(ac<c>,c)","p(+(p,c))","q(q,+(q,q))","~(c,c(J<c,@>))","e(@,@)","c(m?)"],interceptorsByTag:null,leafTags:null,arrayRti:Symbol("$ti"),rttc:{"2;":(a,b)=>c=>c instanceof A.r&&a.b(c.a)&&b.b(c.b)}}
A.ha(v.typeUniverse,JSON.parse('{"ce":"am","b0":"am","a9":"am","it":"aE","c5":{"a7":[],"E":[]},"be":{"E":[]},"bf":{"Q":[]},"am":{"Q":[]},"o":{"n":["1"],"k":["1"],"Q":[],"b":["1"]},"c4":{"bt":[]},"cG":{"o":["1"],"n":["1"],"k":["1"],"Q":[],"b":["1"]},"as":{"H":["1"]},"aU":{"q":[],"al":["q"]},"bd":{"e":[],"q":[],"al":["q"],"E":[]},"c6":{"q":[],"al":["q"],"E":[]},"az":{"c":[],"al":["c"],"E":[]},"an":{"b":["2"]},"b8":{"H":["2"]},"at":{"an":["1","2"],"b":["2"],"b.E":"2"},"bB":{"at":["1","2"],"an":["1","2"],"k":["2"],"b":["2"],"b.E":"2"},"bA":{"x":["2"],"n":["2"],"an":["1","2"],"k":["2"],"b":["2"]},"a8":{"bA":["1","2"],"x":["2"],"n":["2"],"an":["1","2"],"k":["2"],"b":["2"],"x.E":"2","b.E":"2"},"au":{"z":["3","4"],"J":["3","4"],"z.K":"3","z.V":"4"},"aY":{"u":[]},"k":{"b":["1"]},"D":{"k":["1"],"b":["1"]},"bx":{"D":["1"],"k":["1"],"b":["1"],"D.E":"1","b.E":"1"},"aB":{"H":["1"]},"aD":{"b":["2"],"b.E":"2"},"aw":{"aD":["1","2"],"k":["2"],"b":["2"],"b.E":"2"},"bk":{"H":["2"]},"R":{"D":["2"],"k":["2"],"b":["2"],"D.E":"2","b.E":"2"},"ae":{"b":["1"],"b.E":"1"},"aS":{"ae":["1"],"k":["1"],"b":["1"],"b.E":"1"},"bv":{"H":["1"]},"ax":{"k":["1"],"b":["1"],"b.E":"1"},"bb":{"H":["1"]},"r":{"b2":[],"ao":[]},"b9":{"J":["1","2"]},"av":{"b9":["1","2"],"J":["1","2"]},"bC":{"b":["1"],"b.E":"1"},"ai":{"H":["1"]},"aP":{"ad":["1"],"ac":["1"],"k":["1"],"b":["1"]},"ba":{"aP":["1"],"ad":["1"],"ac":["1"],"k":["1"],"b":["1"]},"bc":{"aP":["1"],"ad":["1"],"ac":["1"],"k":["1"],"b":["1"]},"bq":{"u":[]},"c7":{"u":[]},"cl":{"u":[]},"ak":{"aT":[]},"bT":{"aT":[]},"cj":{"aT":[]},"ci":{"aT":[]},"aO":{"aT":[]},"cg":{"u":[]},"aa":{"z":["1","2"],"dO":["1","2"],"J":["1","2"],"z.K":"1","z.V":"2"},"aA":{"k":["1"],"b":["1"],"b.E":"1"},"bi":{"H":["1"]},"bg":{"aa":["1","2"],"z":["1","2"],"dO":["1","2"],"J":["1","2"],"z.K":"1","z.V":"2"},"b2":{"ao":[]},"aE":{"Q":[],"E":[]},"bl":{"Q":[]},"cd":{"eh":[],"Q":[],"E":[]},"a5":{"aW":["1"],"Q":[]},"ab":{"x":["e"],"a5":["e"],"n":["e"],"aW":["e"],"k":["e"],"Q":[],"b":["e"],"ay":["e"]},"bm":{"ab":[],"x":["e"],"a5":["e"],"n":["e"],"aW":["e"],"k":["e"],"Q":[],"b":["e"],"ay":["e"],"E":[],"x.E":"e"},"bn":{"ab":[],"dS":[],"x":["e"],"a5":["e"],"n":["e"],"aW":["e"],"k":["e"],"Q":[],"b":["e"],"ay":["e"],"E":[],"x.E":"e"},"bo":{"ab":[],"dT":[],"x":["e"],"a5":["e"],"n":["e"],"aW":["e"],"k":["e"],"Q":[],"b":["e"],"ay":["e"],"E":[],"x.E":"e"},"co":{"u":[]},"bH":{"u":[]},"aF":{"ad":["1"],"ac":["1"],"k":["1"],"b":["1"]},"aG":{"H":["1"]},"z":{"J":["1","2"]},"bj":{"fO":["1"],"D":["1"],"k":["1"],"b":["1"],"D.E":"1","b.E":"1"},"bD":{"H":["1"]},"ad":{"ac":["1"],"k":["1"],"b":["1"]},"bG":{"ad":["1"],"ac":["1"],"k":["1"],"b":["1"]},"cq":{"z":["c","@"],"J":["c","@"],"z.K":"c","z.V":"@"},"cr":{"D":["c"],"k":["c"],"b":["c"],"D.E":"c","b.E":"c"},"bh":{"u":[]},"c9":{"u":[]},"c8":{"bU":["m?","c"]},"cb":{"aQ":["m?","c"]},"ca":{"aQ":["c","m?"]},"cm":{"aQ":["c","n<e>"]},"e":{"q":[],"al":["q"]},"n":{"k":["1"],"b":["1"]},"q":{"al":["q"]},"ac":{"k":["1"],"b":["1"]},"c":{"al":["c"]},"cn":{"bZ":[]},"bR":{"u":[]},"by":{"u":[]},"a3":{"u":[]},"bs":{"u":[]},"c1":{"u":[]},"bz":{"u":[]},"ck":{"u":[]},"aZ":{"u":[]},"bV":{"u":[]},"bw":{"u":[]},"b_":{"fR":[]},"dT":{"n":["e"],"k":["e"],"b":["e"]},"fU":{"n":["e"],"k":["e"],"b":["e"]},"dS":{"n":["e"],"k":["e"],"b":["e"]},"bW":{"bu":["aR"]},"c0":{"bu":["n<e>"]},"cu":{"bu":["n<e>"]},"ct":{"bu":["n<e>"]},"p":{"bZ":[]},"O":{"bZ":[]},"a4":{"bZ":[]},"Y":{"bZ":[]}}'))
A.h9(v.typeUniverse,JSON.parse('{"bM":2,"a5":1,"bG":1}'))
var u=(function rtii(){var t=A.a_
return{k:t("O"),W:t("al<@>"),O:t("k<@>"),C:t("u"),Z:t("aT"),U:t("b<@>"),Y:t("b<e>"),x:t("o<n<c?>>"),c:t("o<J<c,@>>"),G:t("o<m>"),_:t("o<+(Y,c?)>"),e:t("o<+(p,c)>"),v:t("o<I>"),s:t("o<c>"),b:t("o<@>"),t:t("o<e>"),q:t("o<c?>"),T:t("be"),m:t("Q"),M:t("a9"),p:t("aW<@>"),R:t("p"),r:t("p(+(p,c))"),A:t("bj<+(q,q)>"),u:t("n<+(Y,c?)>"),w:t("n<I>"),j:t("n<@>"),I:t("n<e>"),P:t("J<c,@>"),f:t("J<@,@>"),B:t("R<+(p,c),p>"),E:t("ab"),a:t("bp"),K:t("m"),J:t("iu"),F:t("+()"),d:t("+(p,c)"),D:t("+(q,q)"),Q:t("ac<c>"),h:t("bu<aR>"),N:t("c"),V:t("c(J<c,@>)"),l:t("E"),o:t("b0"),y:t("a7"),i:t("f_"),z:t("@"),S:t("e"),bc:t("ej<bp>?"),aQ:t("Q?"),g:t("n<@>?"),a5:t("J<@,@>?"),X:t("m?"),cl:t("+(q,q)?"),aD:t("c?"),L:t("cs?"),cG:t("a7?"),dd:t("f_?"),a3:t("e?"),n:t("q?"),H:t("q"),bU:t("~(n<I>)"),cQ:t("~(c,@)")}})();(function constants(){var t=hunkHelpers.makeConstList
B.a1=J.c3.prototype
B.a=J.o.prototype
B.f=J.bd.prototype
B.c=J.aU.prototype
B.m=J.az.prototype
B.a2=J.a9.prototype
B.a3=J.bf.prototype
B.aj=A.bm.prototype
B.ak=A.bn.prototype
B.k=A.bo.prototype
B.N=J.ce.prototype
B.y=J.b0.prototype
B.z=new A.O(0,"SLOW_DOWN")
B.p=new A.O(1,"STEP_DOWN")
B.q=new A.O(2,"PAUSE")
B.e=new A.O(3,"STOP")
B.A=new A.O(4,"EMERGENCY_119")
B.B=new A.O(5,"ASK_RPE")
B.C=new A.O(6,"GUARDIAN_ALERT")
B.D=new A.O(7,"LOUD_PROMPT")
B.E=new A.O(8,"SENSOR_FALLBACK")
B.F=new A.O(9,"SENSOR_RESTORED")
B.P=new A.bb(A.a_("bb<0&>"))
B.G=new A.bY()
B.Q=new A.bY()
B.H=function getTagFallback(o) {
  var s = Object.prototype.toString.call(o);
  return s.substring(8, s.length - 1);
}
B.R=function() {
  var toStringFunction = Object.prototype.toString;
  function getTag(o) {
    var s = toStringFunction.call(o);
    return s.substring(8, s.length - 1);
  }
  function getUnknownTag(object, tag) {
    if (/^HTML[A-Z].*Element$/.test(tag)) {
      var name = toStringFunction.call(object);
      if (name == "[object Object]") return null;
      return "HTMLElement";
    }
  }
  function getUnknownTagGenericBrowser(object, tag) {
    if (object instanceof HTMLElement) return "HTMLElement";
    return getUnknownTag(object, tag);
  }
  function prototypeForTag(tag) {
    if (typeof window == "undefined") return null;
    if (typeof window[tag] == "undefined") return null;
    var constructor = window[tag];
    if (typeof constructor != "function") return null;
    return constructor.prototype;
  }
  function discriminator(tag) { return null; }
  var isBrowser = typeof HTMLElement == "function";
  return {
    getTag: getTag,
    getUnknownTag: isBrowser ? getUnknownTagGenericBrowser : getUnknownTag,
    prototypeForTag: prototypeForTag,
    discriminator: discriminator };
}
B.W=function(getTagFallback) {
  return function(hooks) {
    if (typeof navigator != "object") return hooks;
    var userAgent = navigator.userAgent;
    if (typeof userAgent != "string") return hooks;
    if (userAgent.indexOf("DumpRenderTree") >= 0) return hooks;
    if (userAgent.indexOf("Chrome") >= 0) {
      function confirm(p) {
        return typeof window == "object" && window[p] && window[p].name == p;
      }
      if (confirm("Window") && confirm("HTMLElement")) return hooks;
    }
    hooks.getTag = getTagFallback;
  };
}
B.S=function(hooks) {
  if (typeof dartExperimentalFixupGetTag != "function") return hooks;
  hooks.getTag = dartExperimentalFixupGetTag(hooks.getTag);
}
B.V=function(hooks) {
  if (typeof navigator != "object") return hooks;
  var userAgent = navigator.userAgent;
  if (typeof userAgent != "string") return hooks;
  if (userAgent.indexOf("Firefox") == -1) return hooks;
  var getTag = hooks.getTag;
  var quickMap = {
    "BeforeUnloadEvent": "Event",
    "DataTransfer": "Clipboard",
    "GeoGeolocation": "Geolocation",
    "Location": "!Location",
    "WorkerMessageEvent": "MessageEvent",
    "XMLDocument": "!Document"};
  function getTagFirefox(o) {
    var tag = getTag(o);
    return quickMap[tag] || tag;
  }
  hooks.getTag = getTagFirefox;
}
B.U=function(hooks) {
  if (typeof navigator != "object") return hooks;
  var userAgent = navigator.userAgent;
  if (typeof userAgent != "string") return hooks;
  if (userAgent.indexOf("Trident/") == -1) return hooks;
  var getTag = hooks.getTag;
  var quickMap = {
    "BeforeUnloadEvent": "Event",
    "DataTransfer": "Clipboard",
    "HTMLDDElement": "HTMLElement",
    "HTMLDTElement": "HTMLElement",
    "HTMLPhraseElement": "HTMLElement",
    "Position": "Geoposition"
  };
  function getTagIE(o) {
    var tag = getTag(o);
    var newTag = quickMap[tag];
    if (newTag) return newTag;
    if (tag == "Object") {
      if (window.DataView && (o instanceof window.DataView)) return "DataView";
    }
    return tag;
  }
  function prototypeForTagIE(tag) {
    var constructor = window[tag];
    if (constructor == null) return null;
    return constructor.prototype;
  }
  hooks.getTag = getTagIE;
  hooks.prototypeForTag = prototypeForTagIE;
}
B.T=function(hooks) {
  var getTag = hooks.getTag;
  var prototypeForTag = hooks.prototypeForTag;
  function getTagFixed(o) {
    var tag = getTag(o);
    if (tag == "Document") {
      if (!!o.xmlVersion) return "!Document";
      return "!HTMLDocument";
    }
    return tag;
  }
  function prototypeForTagFixed(tag) {
    if (tag == "Document") return null;
    return prototypeForTag(tag);
  }
  hooks.getTag = getTagFixed;
  hooks.prototypeForTag = prototypeForTagFixed;
}
B.I=function(hooks) { return hooks; }

B.b=new A.c8()
B.r=new A.cP()
B.X=new A.cm()
B.Z=new A.Y(2,"SHOW_119")
B.l=new A.a4(0,"ASK_OK")
B.K=new A.a4(1,"RESTING_OK")
B.u=new A.a4(2,"GUARDIAN_ALERTED")
B.v=new A.a4(3,"SHOW_119")
B.L=new A.a4(4,"CALLING_119")
B.M=new A.a4(5,"GUARDIAN_119")
B.a4=new A.ca(null)
B.a5=new A.cb(null)
B.h=new A.p(0,"GREEN")
B.n=new A.p(1,"YELLOW")
B.i=new A.p(2,"REMEASURE")
B.o=new A.p(3,"RED")
B.a6=new A.p(4,"BLOCKED")
B.a7=new A.p(5,"EMERGENCY")
B.w=t([B.h,B.n,B.i,B.o,B.a6,B.a7],A.a_("o<p>"))
B.a0=new A.Y(5,"GUARDIAN_CALL_119")
B.av=new A.r(B.a0,"EM_119_NO_CONFIRM")
B.a8=t([B.av],u._)
B.a9=t([1116352408,1899447441,3049323471,3921009573,961987163,1508970993,2453635748,2870763221,3624381080,310598401,607225278,1426881987,1925078388,2162078206,2614888103,3248222580,3835390401,4022224774,264347078,604807628,770255983,1249150122,1555081692,1996064986,2554220882,2821834349,2952996808,3210313671,3336571891,3584528711,113926993,338241895,666307205,773529912,1294757372,1396182291,1695183700,1986661051,2177026350,2456956037,2730485921,2820302411,3259730800,3345764771,3516065817,3600352804,4094571909,275423344,430227734,506948616,659060556,883997877,958139571,1322822218,1537002063,1747873779,1955562222,2024104815,2227730452,2361852424,2428436474,2756734187,3204031479,3329325298],u.t)
B.a_=new A.Y(3,"DIAL_119")
B.ar=new A.r(B.a_,"EM_119_CONFIRMED")
B.t=new A.Y(4,"NOTIFY_GUARDIAN")
B.as=new A.r(B.t,"EM_119_CONFIRMED")
B.aa=t([B.ar,B.as],u._)
B.J=new A.Y(0,"REST_GUIDANCE")
B.ao=new A.r(B.J,"EM_USER_OK")
B.ab=t([B.ao],u._)
B.at=new A.r(B.t,"EM_NO_RESPONSE")
B.ac=t([B.at],u._)
B.au=new A.r(B.t,"EM_USER_NOT_OK")
B.ad=t([B.au],u._)
B.ae=t([],u.v)
B.aN=t([],u.s)
B.x=t([],u.b)
B.j=t([],u._)
B.af=t([B.z,B.p,B.q,B.e,B.A,B.B,B.C,B.D,B.E,B.F],A.a_("o<O>"))
B.ap=new A.r(B.J,null)
B.Y=new A.Y(1,"ASK_OK")
B.aq=new A.r(B.Y,null)
B.ag=t([B.ap,B.aq],u._)
B.ah=t(["systolic","diastolic","resting_hr"],u.s)
B.am={}
B.d=new A.av(B.am,[],A.a_("av<c,@>"))
B.al={systolic:0,diastolic:1,resting_hr:2}
B.ai=new A.av(B.al,["systolic_max","diastolic_max","resting_hr_max"],A.a_("av<c,c>"))
B.aw=new A.r(B.h,"DOCTOR_LIMIT_LOOSER_IGNORED")
B.ax=new A.r(B.n,"PRE_YELLOW_CONDITION")
B.ay=new A.r(B.n,"PRE_YELLOW_SYMPTOM")
B.az=new A.r(B.i,"PRE_BP_SOURCE_NOT_ALLOWED")
B.aA=new A.r(B.i,"PRE_HR_SOURCE_LOW_GRADE")
B.O=new A.r(B.i,"PRE_IMPLAUSIBLE_VALUE")
B.aB=new A.r(B.i,"PRE_MISSING_VALUE")
B.aC=new A.r(B.o,"PRE_OVER_DOCTOR_LIMIT")
B.aD=new A.r(B.o,"PRE_RED_CONDITION")
B.aE=new A.r(B.o,"PRE_RED_SYMPTOM")
B.aF=new A.bc([B.K,B.u,B.L,B.M],A.a_("bc<a4>"))
B.an={GREEN:0,YELLOW:1,RED:2}
B.aG=new A.ba(B.an,3,A.a_("ba<c>"))
B.aH=A.bO("ip")
B.aI=A.bO("eh")
B.aJ=A.bO("m")
B.aK=A.bO("fU")
B.aL=A.bO("dS")
B.aM=A.bO("dT")})();(function staticFields(){$.d3=null
$.T=A.t([],u.G)
$.eq=null
$.ef=null
$.ee=null
$.f0=null
$.eY=null
$.f2=null
$.dv=null
$.dB=null
$.e4=null
$.d7=A.t([],A.a_("o<n<m>?>"))
$.b4=null
$.eU=A.dP(u.S,A.a_("ch"))
$.eN=A.dP(u.S,A.a_("bX"))
$.ds=1})();(function lazyInitializers(){var t=hunkHelpers.lazyFinal
t($,"ir","f5",()=>A.dw("_$dart_dartClosure"))
t($,"iq","e9",()=>A.dw("_$dart_dartClosure_dartJSInterop"))
t($,"iH","fi",()=>A.t([new J.c4()],A.a_("o<bt>")))
t($,"iv","f7",()=>A.ah(A.d0({
toString:function(){return"$receiver$"}})))
t($,"iw","f8",()=>A.ah(A.d0({$method$:null,
toString:function(){return"$receiver$"}})))
t($,"ix","f9",()=>A.ah(A.d0(null)))
t($,"iy","fa",()=>A.ah(function(){var $argumentsExpr$="$arguments$"
try{null.$method$($argumentsExpr$)}catch(s){return s.message}}()))
t($,"iB","fd",()=>A.ah(A.d0(void 0)))
t($,"iC","fe",()=>A.ah(function(){var $argumentsExpr$="$arguments$"
try{(void 0).$method$($argumentsExpr$)}catch(s){return s.message}}()))
t($,"iA","fc",()=>A.ah(A.ev(null)))
t($,"iz","fb",()=>A.ah(function(){try{null.$method$}catch(s){return s.message}}()))
t($,"iE","fg",()=>A.ah(A.ev(void 0)))
t($,"iD","ff",()=>A.ah(function(){try{(void 0).$method$}catch(s){return s.message}}()))
t($,"iG","cx",()=>A.e7(B.aJ))
t($,"is","f6",()=>J.fk(B.aj.gW(new Uint16Array(A.eL(A.t([1],u.t)))),0,null).getInt8(0)===1?B.Q:B.G)
t($,"iF","fh",()=>A.w(["load",new A.dc(),"preCheck",new A.dd(),"allowance",new A.de(),"postCheck",new A.df(),"hrLimits",new A.dg(),"monitorNew",new A.dh(),"monitorEvent",new A.di(),"flowNew",new A.dj(),"flowEvent",new A.dk()],u.N,u.V))})();(function nativeSupport(){!function(){var t=function(a){var n={}
n[a]=1
return Object.keys(hunkHelpers.convertToFastObject(n))[0]}
v.getIsolateTag=function(a){return t("___dart_"+a+v.isolateTag)}
var s="___dart_isolate_tags_"
var r=Object[s]||(Object[s]=Object.create(null))
var q="_ZxYxX"
for(var p=0;;p++){var o=t(q+"_"+p+"_")
if(!(o in r)){r[o]=1
v.isolateTag=o
break}}v.dispatchPropertyName=v.getIsolateTag("dispatch_record")}()
hunkHelpers.setOrUpdateInterceptorsByTag({ArrayBuffer:A.aE,SharedArrayBuffer:A.aE,ArrayBufferView:A.bl,DataView:A.cd,Uint16Array:A.bm,Uint32Array:A.bn,Uint8Array:A.bo})
hunkHelpers.setOrUpdateLeafTags({ArrayBuffer:true,SharedArrayBuffer:true,ArrayBufferView:false,DataView:true,Uint16Array:true,Uint32Array:true,Uint8Array:false})
A.a5.$nativeSuperclassTag="ArrayBufferView"
A.bE.$nativeSuperclassTag="ArrayBufferView"
A.bF.$nativeSuperclassTag="ArrayBufferView"
A.ab.$nativeSuperclassTag="ArrayBufferView"})()
Function.prototype.$1=function(a){return this(a)}
Function.prototype.$2=function(a,b){return this(a,b)}
Function.prototype.$0=function(){return this()}
Function.prototype.$4=function(a,b,c,d){return this(a,b,c,d)}
Function.prototype.$1$0=function(){return this()}
Function.prototype.$2$0=function(){return this()}
Function.prototype.$3=function(a,b,c){return this(a,b,c)}
Function.prototype.$1$1=function(a){return this(a)}
convertAllToFastObject(w)
convertToFastObject($);(function(a){if(typeof document==="undefined"){a(null)
return}if(typeof document.currentScript!="undefined"){a(document.currentScript)
return}var t=document.scripts
function onLoad(b){for(var r=0;r<t.length;++r){t[r].removeEventListener("load",onLoad,false)}a(b.target)}for(var s=0;s<t.length;++s){t[s].addEventListener("load",onLoad,false)}})(function(a){v.currentScript=a
var t=A.id
if(typeof dartMainRunner==="function"){dartMainRunner(t,[])}else{t([])}})})()
//# sourceMappingURL=engine.js.map
