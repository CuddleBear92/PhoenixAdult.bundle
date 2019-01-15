import PAsearchSites
import PAgenres

def posterAlreadyExists(posterUrl,metadata):
    for p in metadata.posters.keys():
        Log(p.lower())
        if p.lower() == posterUrl.lower():
            Log("Found " + posterUrl + " in posters collection")
            return True

    for p in metadata.art.keys():
        if p.lower() == posterUrl.lower():
            return True
    return False

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(searchSiteID) + encodedTitle)
    Log(PAsearchSites.getSearchSearchURL(searchSiteID) + encodedTitle)
    Log("Results Found: "+str(len(searchResults.xpath('//div[@class="tlcDetails"]'))))
    for searchResult in searchResults.xpath('//div[@class="tlcDetails"]'):
        titleNoFormatting = searchResult.xpath('.//a[1]')[0].text_content().strip()
        curID = searchResult.xpath('.//a[1]')[0].get('href').replace('/','_').replace('?','!')
        try:
            releaseDate = parse(searchResult.xpath('.//div[@class="tlcSpecs"]/span[@class="tlcSpecsDate"]/span[@class="tlcDetailsValue"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        except:
            releaseDate = ''
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())

        if searchSiteID == 278 or (searchSiteID >= 285 and searchSiteID <= 287):
            network = 'XEmpire'
        elif searchSiteID == 329 or (searchSiteID >= 351 and searchSiteID <= 354):
            network = 'Blowpass'
        elif searchSiteID == 331 or (searchSiteID >= 355 and searchSiteID <= 360):
            network = 'Fantasy Massage'
        elif searchSiteID == 330 or searchSiteID == 332 or (searchSiteID >= 361 and searchSiteID <= 365):
            network = 'Mile High Network'
        elif searchSiteID >= 365 and searchSiteID <= 372:
            network = '21Sextury'
        elif searchSiteID == 183 or (searchSiteID >= 373 and searchSiteID <= 374):
            network = '21Naturals'
        elif searchSiteID == 53 or (searchSiteID >= 375 and searchSiteID <= 379):
            network = 'Girlsway'
        elif searchSiteID >= 383 and searchSiteID <= 386:
            network = 'Fame Digital'
        elif searchSiteID >= 387 and searchSiteID <= 392:
            network = 'Open Life Network'
        elif searchSiteID == 281:
            network = 'PureTaboo'
        elif searchSiteID == 380:
            network = 'Girlfriends Films'
        elif searchSiteID == 381:
            network = 'Burning Angel'
        elif searchSiteID == 277:
            network = 'Evil Angel'
        elif searchSiteID == 382:
            network = 'Pretty Dirty'

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+network+"/"+PAsearchSites.getSearchSiteName(searchSiteID)+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    if siteID == 278 or (siteID >= 285 and siteID <= 287):
        metadata.studio = 'XEmpire'
    elif siteID == 329 or (siteID >= 351 and siteID <= 354):
        metadata.studio = 'Blowpass'
    elif siteID == 331 or (siteID >= 355 and siteID <= 360):
        metadata.studio = 'Fantasy Massage'
    elif siteID == 330 or siteID == 332 or (siteID >= 361 and siteID <= 365):
        metadata.studio = 'Mile High Network'
    elif siteID >= 365 and siteID <= 372:
        metadata.studio = '21Sextury'
    elif siteID == 183 or (siteID >= 373 and siteID <= 374):
        metadata.studio = '21Naturals'
    elif siteID == 53 or (siteID >= 375 and siteID <= 379):
        metadata.studio = 'Girlsway'
    elif siteID >= 383 and siteID <= 386:
        metadata.studio = 'Fame Digital'
    elif siteID >= 387 and siteID <= 392:
        metadata.studio = 'Open Life Network'
    elif siteID == 281:
        metadata.studio = 'PureTaboo'
    elif siteID == 380:
        metadata.studio = 'Girlfriends Films'
    elif siteID == 381:
        metadata.studio = 'Burning Angel'
    elif siteID == 277:
        metadata.studio = 'Evil Angel'
    elif siteID == 382:
        metadata.studio = 'Pretty Dirty'
    temp = str(metadata.id).split("|")[0].replace('_','/')
    url = (PAsearchSites.getSearchBaseURL(siteID) + temp).replace("https:","http:")
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    try:
        paragraph = detailsPageElements.xpath('//meta[@name="twitter:description"]')[0].get('content').strip()
    except:
        try:
            paragraph = detailsPageElements.xpath('//div[@class="sceneDesc bioToRight showMore"]')[0].text_content().strip()
            paragraph = paragraph[20:]
        except:
            try:
                paragraph = detailsPageElements.xpath('//div[@class="sceneDescText"]')[0].text_content().strip()
            except:
                pass
    metadata.summary = paragraph.strip()
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    try:
        metadata.title = detailsPageElements.xpath('//meta[@name="twitter:title"]')[0].get('content').strip()
    except:
        metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    try:
        dvdLink = detailsPageElements.xpath('//a[contains(@class,"dvdLink")][1]')[0].get('title').strip()
        metadata.collections.add(dvdLink)
    except:
        pass

    # Director
    metadata.directors.clear()
    try:
        directors = detailsPageElements.xpath('//div[@class="sceneCol sceneColDirectors"]//a')
        Log("Directors found: "+str(len(directors)))
        for director in directors:
            Log("Director: "+str(director.text_content().strip()))
            metadata.directors.add(director.text_content().strip())
    except:
        pass

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="sceneCol sceneColCategories"]//a | //div[@class="sceneCategories"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="updatedDate"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="sceneCol sceneColActors"]//a | //div[@class="sceneCol sceneActors"]//a')
    if metadata.title == 'Kennedy Leigh' and metadata.tagline == 'Only Teen Blowjobs':
        movieActors.addActor('Kennedy Leigh','')

    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL).replace("https:","http:"))
            actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]')[0].get("src").replace("https:","http:")
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters
    try:
        twitterBG = detailsPageElements.xpath('//meta[@name="twitter:image"]')[0].get('content').replace("https:","http:")
        art.append(twitterBG)
    except:
        picScript = detailsPageElements.xpath('//script[contains(text(),"picPreview")]')[0].text_content()
        alpha = picScript.find('"picPreview":"')+14
        omega = picScript.find('"',alpha)
        Log('BG in <script>: '+picScript[alpha:omega].replace('\\',''))
        art.append(picScript[alpha:omega].replace('\\','').replace("https:","http:"))

    try:
        sceneImg = detailsPageElements.xpath('//img[@class="sceneImage"]')[0].get('src').replace("https:","http:")
        art.append(sceneImg)
    except:
        pass
    
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID)+detailsPageElements.xpath('//a[@class="controlButton GA_Track GA_Track_Action_Pictures GA_Track_Category_Player GA GA_Click GA_Id_ScenePlayer_Pictures"]')[0].get('href').replace("https:","http:")
        photoPage = HTML.ElementFromURL(photoPageUrl)
        unlockedPhotos = photoPage.xpath('//a[@class="imgLink"] | //a[@class="imgLink pgUnlocked"]')
        for unlockedPhoto in unlockedPhotos:
            art.append(unlockedPhoto.get('href').replace("https:","http:"))
    except:
        pass

    j = 1
    for posterUrl in art:
        if not posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': photoPageUrl}).content, sort_order = j)
                if(width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': photoPageUrl}).content, sort_order = j)
                j = j + 1
            except Exception as e:
                Log("Error: " + str(e))

    return metadata