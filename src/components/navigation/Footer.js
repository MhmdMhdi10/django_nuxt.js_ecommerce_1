import { Footer } from 'flowbite-react';
import { BsInstagram , BsWhatsapp, BsTelegram, BsTelephone } from 'react-icons/bs';

export default function FooterWithLogo() {
  return (
    <Footer container className={'rounded-sm'}>
      <div className="w-full ">
        <div className="grid w-full justify-between sm:flex sm:justify-between md:flex md:grid-cols-1">
          <div className={'flex gap-2'}>
            <Footer.Brand
              alt="Flowbite Logo"
              href="https://flowbite.com"
              name={'\u00A0 نوین صنعت تسلا'}
              src="https://flowbite.com/docs/images/logo.svg"
            />

          </div>
          <div className="grid grid-cols-2 gap-8 mt-6 sm:mt-4 sm:grid-cols-3  text-right">
            <div>
              <Footer.Title title="با نوین صنعت تسلا" />
              <Footer.LinkGroup col>
                <Footer.Link href="#" className={'md:mr-0'}>
                  درباره ما
                </Footer.Link>
                <Footer.Link href="#" className={'md:mr-0'}>
                  تماس با ما
                </Footer.Link>
              </Footer.LinkGroup>
            </div>
            <div>
              <Footer.Title title="خدمات وبسایت" />
              <Footer.LinkGroup col>
                <Footer.Link href="#" className={'md:mr-0'}>
                  محصولات
                </Footer.Link>
                <Footer.Link href="#" className={'md:mr-0'}>
                  بلاگ
                </Footer.Link>
              </Footer.LinkGroup>
            </div>
            <div>
              <Footer.Title title="خدمات مشتریان" />
              <Footer.LinkGroup col>
                <Footer.Link href="#" className={'md:mr-0'}>
                  رویه ی بازگرداندن کالا
                </Footer.Link>
                <Footer.Link href="#" className={'md:mr-0'}>
                  قوانین و مقررات
                </Footer.Link>
                <Footer.Link href="#" className={'md:mr-0'}>
                  حریم خصوصی
                </Footer.Link>
              </Footer.LinkGroup>
            </div>
          </div>
        </div>
        <Footer.Divider />
        <div className={'grid grid-cols-2 lg:grid-cols-4 gap-10 text-sm lg:text-md'}>
          <div className={'dark:text-white'}>
            <p>آدرس: تهران خیابان فردوسی جنوبی کوچه باربد مجتمع تجاری باربد پلاک ۵</p><br/>
            <p>شماره تماس: <span dir={'ltr'} className={'text-lg'}>۳۳ ۱۱ ۰۶۱۸ - ۳۳ ۱۱ ۰۶۱۸ - ۰۹۱۲ ۳۴۵ ۶۷۸۹&nbsp;</span>  </p>
          </div>

          <div className={'dark:text-white'}>
            <p>در صورت تمایل به ثبت سفارش تلفنی یا حضوری  میتوانید با ما تماس بگیرید یا به آدرس مندرج مراجعه کنید.</p>
            <p>برای درخواست پیش فاکتور میتوانید محصولات خود را انتخاب کنید و در سبد خرید بر روی گزینه درخواست پیش فاکتور کلیک کنید.</p>
          </div>

          <div className={'dark:text-white col-span-2 gap-10 float-left grid grid-cols-2 lg:grid-cols-4 justify-center items-center'}>

            <div dir={'ltr'} className={'ml-6 float-left flex justify-center items-center'}>
              <div className={'mr-2'}>
                <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                  <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.3" d="M15.5 10.25a2.25 2.25 0 1 0 0 4.5 2.25 2.25 0 0 0 0-4.5Zm0 0a2.225 2.225 0 0 0-1.666.75H12m3.5-.75a2.225 2.225 0 0 1 1.666.75H19V7m-7 4V3h5l2 4m-7 4H6.166a2.225 2.225 0 0 0-1.666-.75M12 11V2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v9h1.834a2.225 2.225 0 0 1 1.666-.75M19 7h-6m-8.5 3.25a2.25 2.25 0 1 0 0 4.5 2.25 2.25 0 0 0 0-4.5Z"/>
                </svg>
              </div>
              <div className={'text-[12px]'}>
                <p>ارسال به تمام<br/> نقاط کشور</p>
              </div>
            </div>

            <div dir={'ltr'} className={'ml-6 float-left flex justify-center items-center'}>
              <div className={'mr-2'}>
                <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 21 19">
                  <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 4C5.5-1.5-1.5 5.5 4 11l7 7 7-7c5.458-5.458-1.542-12.458-7-7Z"/>
                </svg>
              </div>
              <div className={'text-[12px]'}>
                <p>تضمین سلامت و<br/>  اصل بودن کالا</p>
              </div>
            </div>

            <div dir={'ltr'} className={'ml-6 float-left flex justify-center items-center'}>
              <div className={'mr-2'}>
                <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 18">
                  <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 13v-3a9 9 0 1 0-18 0v3m2-3h3v7H3a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2Zm11 0h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-3v-7Z"/>
                </svg>
              </div>
              <div className={'text-[12px]'}>
                <p>مشاوره ی<br/> رایگان خرید</p>
              </div>
            </div>

            <div dir={'ltr'} className={'ml-6 float-left flex justify-center items-center'}>
              <div className={'mr-2'}>
                <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 21 21">
                  <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m6.072 10.072 2 2 6-4m3.586 4.314.9-.9a2 2 0 0 0 0-2.828l-.9-.9a2 2 0 0 1-.586-1.414V5.072a2 2 0 0 0-2-2H13.8a2 2 0 0 1-1.414-.586l-.9-.9a2 2 0 0 0-2.828 0l-.9.9a2 2 0 0 1-1.414.586H5.072a2 2 0 0 0-2 2v1.272a2 2 0 0 1-.586 1.414l-.9.9a2 2 0 0 0 0 2.828l.9.9a2 2 0 0 1 .586 1.414v1.272a2 2 0 0 0 2 2h1.272a2 2 0 0 1 1.414.586l.9.9a2 2 0 0 0 2.828 0l.9-.9a2 2 0 0 1 1.414-.586h1.272a2 2 0 0 0 2-2V13.8a2 2 0 0 1 .586-1.414Z"/>
                </svg>
              </div>
              <div className={'text-[12px]'}>
                <p>تضمین بهترین<br/> قیمت و کیفیت</p>
              </div>
            </div>

          </div>

        </div>
        <Footer.Divider />
        <div className="w-full sm:flex sm:items-center sm:justify-between">
          <Footer.Copyright
            by={'\u00A0 تمامی حقوق مادی و معنوی این سایت متعلق به فروشگاه اینترنتی نوین صنعت تسلا می باشد.  \u00A0'}
            href="#"
            year={2023}
          />
          <div className="mt-4 flex space-x-6 sm:mt-0 sm:justify-center" >
            <div className={'ml-6'}>
              <Footer.Icon
                href="#"
                icon={BsTelephone}
              />
            </div>
            <Footer.Icon
              href="#"
              icon={BsInstagram}
            />
            <Footer.Icon
              href="#"
              icon={BsTelegram}
            />
            <Footer.Icon
              href="#"
              icon={BsWhatsapp}
            />
          </div>
        </div>
      </div>
    </Footer>
  )
}



